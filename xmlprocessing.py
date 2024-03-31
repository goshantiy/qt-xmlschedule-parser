import sys
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem,
                             QComboBox, QVBoxLayout, QWidget, QPushButton, QFileDialog,
                             QHBoxLayout, QLabel)


class XMLProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.tree = ET.parse(filename) if filename else None
        self.root = self.tree.getroot() if self.tree else None

    def get_elements(self, path):
        return self.root.findall(path) if self.root else []

    def get_element_text(self, element, tag):
        child = element.find(tag)
        return child.text if child is not None else ''
    
class ClassProcessor(XMLProcessor):
    def __init__(self, filename):
        super().__init__(filename)

    def get_classes(self):
        return self.get_elements("./classes/class")

    def get_names(self):
        return [self.get_element_text(class_element, "name") for class_element in self.get_classes()]
    
class SubjectProcessor(XMLProcessor):
    def get_subjects(self):
        return self.get_elements("./subjects/subject")

    def get_subject_names(self):
        return [self.get_element_text(subject, "short_name") for subject in self.get_subjects()]


class RoomProcessor(XMLProcessor):
    def get_rooms(self):
        return self.get_elements("./rooms/room")

    def get_names(self):
        return [self.get_element_text(room, "name") for room in self.get_rooms()]


class ChairProcessor(XMLProcessor):
    def get_chairs(self):
        return self.get_elements("./chairs/chair")

    def get_names(self):
        return [self.get_element_text(chair, "short_name") for chair in self.get_chairs()]


class TeacherProcessor(XMLProcessor):
    def get_teachers(self):
        return self.get_elements("./teachers/teacher")

    def get_names(self):
        # This could be adjusted based on the structure of your XML and what you consider to be the 'name'
        return [f"{self.get_element_text(teacher, 'surname')} {self.get_element_text(teacher, 'first_name')}" for teacher in self.get_teachers()]


class SchedProcessor(XMLProcessor):
    def get_scheds(self):
        return self.get_elements("./scheds/sched")
    def get_names(self):
        return

    # Further processing can be added as per requirement


class StudyTypeProcessor(XMLProcessor):
    def get_study_types(self):
        return self.get_elements("./study_types/study_type")

    def get_names(self):
        return [self.get_element_text(study_type, "short_name") for study_type in self.get_study_types()]
