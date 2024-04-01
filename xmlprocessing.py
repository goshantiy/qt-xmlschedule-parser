import sys
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem,
                             QComboBox, QVBoxLayout, QWidget, QPushButton, QFileDialog,
                             QHBoxLayout, QLabel)


class XMLProcessor:
    def __init__(self, source):
        if isinstance(source, str):
            self.tree = ET.parse(source)
            self.root = self.tree.getroot()
        else:
            self.root = source
            self.tree = None

    def get_elements(self, path):
        return self.root.findall(path) if self.root else []

    def get_element_text(self, element, tag):
        child = element.find(tag)
        return child.text if child is not None else ''
    
class ClassProcessor(XMLProcessor):
    def __init__(self, xml_string):
        super().__init__(xml_string)

    def get_classes(self):
        return self.get_elements("./classes/class")

    def get_names(self):
        return [self.get_element_text(class_element, "name") for class_element in self.get_classes()]

    def parse_class_details(self):
        classes_details = []
        for class_element in self.get_classes():
            class_details = {
                'id': self.get_element_text(class_element, 'id'),
                'name': self.get_element_text(class_element, 'name'),
                'session': self.get_element_text(class_element, 'session'),
                'student': self.get_element_text(class_element, 'student'),
                'min_lessons_per_day': self.get_element_text(class_element, 'min_lessons_per_day'),
                'max_lessons_per_day': self.get_element_text(class_element, 'max_lessons_per_day'),
                'max_load_per_week': self.get_element_text(class_element, 'max_load_per_week'),
                'work_hours': self.parse_work_hours(class_element.find('work_hours'))
            }
            classes_details.append(class_details)
        return classes_details

    def parse_work_hours(self, work_hours_element):
        work_hours = {}
        for week in work_hours_element:
            week_index = week.attrib['i']
            days_hours = {}
            for day in week:
                day_index = day.attrib['i']
                hours = day.text
                days_hours[day_index] = hours
            work_hours[week_index] = days_hours
        return work_hours
    
class SubjectProcessor(XMLProcessor):
    def get_subjects(self):
        return self.get_elements("./subjects/subject")

    def get_subject_names(self):
        return [self.get_element_text(subject, "short_name") for subject in self.get_subjects()]


class RoomProcessor(XMLProcessor):
    def __init__(self, xml_string):
        super().__init__(xml_string)
        self.rooms = self.parse_rooms()

    def get_rooms(self):
        return self.get_elements("./room")

    def parse_rooms(self):
        rooms_dict = {}
        for room in self.get_rooms():
            room_id = self.get_element_text(room, 'id')
            name = self.get_element_text(room, 'name')
            capacity = self.get_element_text(room, 'capacity')
            building = self.get_element_text(room, 'building')
            chair_id = self.get_element_text(room, 'chair_id')
            work_hours = self.parse_work_hours(room.find('work_hours'))
            rooms_dict[room_id] = {
                'name': name,
                'capacity': capacity,
                'building': building,
                'chair_id': chair_id,
                'work_hours': work_hours
            }
        return rooms_dict

    def parse_work_hours(self, work_hours_element):
        work_hours = {}
        for week in work_hours_element:
            week_index = week.attrib['i']
            days = {}
            for day in week:
                day_index = day.attrib['i']
                hours = day.text
                days[day_index] = hours
            work_hours[week_index] = days
        return work_hours



class ChairProcessor(XMLProcessor):
    def __init__(self, xml_string):
        super().__init__(xml_string)
        self.chairs = self.parse_chairs()

    def get_chairs(self):
        return self.get_elements("./chair")

    def parse_chairs(self):
        chairs_dict = {}
        for chair in self.get_chairs():
            chair_id = self.get_element_text(chair, 'id')
            short_name = self.get_element_text(chair, 'short_name')
            full_name = self.get_element_text(chair, 'full_name')
            chairs_dict[chair_id] = {
                'short_name': short_name,
                'full_name': full_name
            }
        return chairs_dict

    def get_names(self):
        return [chair['short_name'] for chair in self.chairs.values()]



class TeacherProcessor(XMLProcessor):
    def __init__(self, xml_string):
        super().__init__(xml_string)
        self.teachers = self.parse_teachers()

    def get_teachers(self):
        return self.get_elements("./teacher")

    def parse_teachers(self):
        teachers_dict = {}
        for teacher in self.get_teachers():
            teacher_id = self.get_element_text(teacher, 'person/id')
            surname = self.get_element_text(teacher, 'person/surname')
            first_name = self.get_element_text(teacher, 'person/first_name')
            chair_id = self.get_element_text(teacher, 'chair_id')
            work_hours = self.parse_work_hours(teacher.find('work_hours'))
            teachers_dict[teacher_id] = {
                'surname': surname,
                'first_name': first_name,
                'chair_id': chair_id
            }
        return teachers_dict
    
    def parse_work_hours(self, work_hours_element):
        total_hours = 0
        for week in work_hours_element:
            for day in week:
                hours = int(day.text)
                # Подсчет количества '1' в двоичном представлении часов
                total_hours += bin(hours).count('1')
        return total_hours

    def get_names(self):
        return [f"{teacher['surname']} {teacher['first_name']}" for teacher in self.teachers.values()]



class SchedProcessor(XMLProcessor):
    def __init__(self, xml_string):
        super().__init__(xml_string)
        self.scheds = self.parse_scheds()

    def get_scheds(self):
        return self.get_elements("./sched")

    def parse_scheds(self):
        scheds_list = []
        for sched in self.get_scheds():
            day = self.get_element_text(sched, 'day')
            hour = self.get_element_text(sched, 'hour')
            group = self.get_element_text(sched, 'group')
            load_id = self.get_element_text(sched, 'load_id')
            room_id = self.get_element_text(sched, 'room_id')
            fixed = self.get_element_text(sched, 'fixed')
            begin_date = self.get_element_text(sched, 'begin_date')
            end_date = self.get_element_text(sched, 'end_date')
            scheds_list.append({
                'day': day,
                'hour': hour,
                'group': group,
                'load_id': load_id,
                'room_id': room_id,
                'fixed': fixed,
                'begin_date': begin_date,
                'end_date': end_date
            })

        return scheds_list


class PlanProcessor(XMLProcessor):
    def __init__(self, xml_string):
        super().__init__(xml_string)
        self.plans = self.parse_plans()

    def get_plans(self):
        return self.get_elements("./plan")

    def parse_plans(self):
        plans_list = []
        for plan in self.get_plans():
            plan_id = self.get_element_text(plan, 'id')
            speciality_id = self.get_element_text(plan, 'speciality_id')
            subject_id = self.get_element_text(plan, 'subject_id')
            semester_plans = self.parse_semester_plans(plan.find('semester_plans'))
            
            plans_list.append({
                'plan_id': plan_id,
                'speciality_id': speciality_id,
                'subject_id': subject_id,
                'semester_plans': semester_plans
            })
        return plans_list

    def parse_semester_plans(self, semester_plans_element):
        semester_plans_list = []
        for semester_plan in semester_plans_element:
            semester = self.get_element_text(semester_plan, 'semester')
            study_type_list = self.parse_study_type_list(semester_plan.find('study_type_list'))
            
            semester_plans_list.append({
                'semester': semester,
                'study_type_list': study_type_list
            })
        return semester_plans_list

    def parse_study_type_list(self, study_type_list_element):
        study_types = []
        for element in study_type_list_element:
            int1 = self.get_element_text(element, 'int1')
            int2 = self.get_element_text(element, 'int2')
            
            study_types.append({'type': int1, 'hours': int2})
        return study_types
