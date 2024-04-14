import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QComboBox, QVBoxLayout, QWidget, QPushButton, QFileDialog, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
import xml.etree.ElementTree as ET
from xmlprocessing import *
from loadtable import *
from roomloadtable import *
from roomavailabilitychecker import *
from teacherload import *
from efficiency import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 150, 150)  # Установка размера и позиции окна
        self.class_processor = {}
        self.teacher_processor = {}
        self.room_processor = {}
        self.chair_processor = {}
        self.sched_processor = {}
        self.plan_processor = {}

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.file_selector_layout = QHBoxLayout()
        self.layout.addLayout(self.file_selector_layout)

        self.file_selected_label = QLabel("Выбранный файл:")
        self.file_selector_button = QPushButton("Выбрать файл")
        self.file_selector_button.clicked.connect(self.select_file)
        self.file_selector_layout.addWidget(self.file_selected_label)
        self.file_selector_layout.addWidget(self.file_selector_button)

        # Стилизация
        self.central_widget.setStyleSheet("""
            QLabel, QPushButton {
                font-size: 16px;  /* Увеличиваем шрифт */
                font-family: Arial, sans-serif;  /* Задаем красивый и читаемый шрифт */
            }
            QPushButton {
                min-height: 30px;  /* Увеличиваем размер кнопок */
            }
        """)


        # Добавляем макет и виджеты для расчета нагрузки
        self.calc_load_layout = QVBoxLayout()  # Создаем новый горизонтальный макет для элементов управления расчетом нагрузки
        self.layout.addLayout(self.calc_load_layout)  # Добавляем новый макет в основной вертикальный макет

        # Создаем пространства для центрирования метки
        left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.calc_load_label = QLabel("Нагрузка кафедр:")  # Метка для кнопки расчета
        self.calc_load_button = QPushButton("Нагрузка кафедр")  # Кнопка для инициации расчета
        self.calc_load_button.clicked.connect(self.calculate_and_sort_load_by_department)  # Подключаем событие клика к методу расчета

        self.calc_room_load_label = QLabel("Нагрузка аудиторий:")  # Метка для кнопки расчета, центрирована
        self.calc_room_load_button = QPushButton("Нагрузка аудиторий")  # Кнопка для инициации расчета
        self.calc_room_load_button.clicked.connect(self.get_rooms_load)  # Подключаем событие клика к методу расчета

        self.calc_room_available_button = QPushButton("Доступность аудитории")  # Кнопка для инициации расчета
        self.calc_room_available_button.clicked.connect(self.get_rooms_availability)  # Подключаем событие клика к методу расчета
        
        self.calc_load_layout.addSpacerItem(left_spacer)  # Добавляем левый спейсер
        self.calc_load_layout.addWidget(self.calc_load_label)  # Добавляем метку в макет
        self.calc_load_layout.addWidget(self.calc_load_button)  # Добавляем кнопку в макет
        self.calc_load_layout.addWidget(self.calc_room_load_label)  # Добавляем метку в макет
        self.calc_load_layout.addWidget(self.calc_room_load_button)  # Добавляем кнопку в макет
        self.calc_load_layout.addWidget(self.calc_room_available_button)  # Добавляем кнопку в макет
        self.calc_load_layout.addSpacerItem(right_spacer)  # Добавляем правый спейсер

        self.teacher_load_label = QLabel("Нагрузка преподавателей: ")
        self.teacher_load_button = QPushButton("Нагрузка преподавателей")
        self.teacher_load_button.clicked.connect(self.show_teacher_load)
        self.calc_load_layout.addWidget(self.teacher_load_label)
        self.calc_load_layout.addWidget(self.teacher_load_button)

        self.eff_group_button = QPushButton("Эффективность расписания группы")
        self.eff_teacher_button = QPushButton("Эффективность расписания преподавателей")

        self.eff_group_button.clicked.connect(self.open_group_eff_form)
        self.eff_teacher_button.clicked.connect(self.open_teacher_eff_form)

        self.layout.addWidget(self.eff_group_button)
        self.layout.addWidget(self.eff_teacher_button)


        self.setWindowTitle("XML Viewer")
        self.filename = ""

    def select_file(self):
        options = QFileDialog.Options()
        self.filename, _ = QFileDialog.getOpenFileName(self, "Выбрать XML файл", "", "XML Files (*.xml)", options=options)
        if self.filename:
            self.file_selected_label.setText(f"Выбранный файл: {self.filename}")
            self.parse_file()  

    def open_group_eff_form(self):
        group_items = ["Группа 1", "Группа 2", "Группа 3"]  # Пример данных
        self.group_eff_form = EfficiencyForm(group_items, "Эффективность расписания группы")
        self.group_eff_form.show()

    def open_teacher_eff_form(self):
        teacher_items = []
        for teacher_data in self.teacher_processor.values():
            # Собираем части имени, пропуская пустые значения
            name_parts = [part for part in [teacher_data['surname'], teacher_data['first_name'], teacher_data['second_name']] if part]
            # Объединяем части в полное имя
            full_name = ' '.join(name_parts)
            teacher_items.append(full_name)

        # Создаем и показываем форму с данными преподавателей
        self.teacher_eff_form = EfficiencyForm(teacher_items, "Эффективность расписания преподавателей")
        self.teacher_eff_form.show()


            
    def parse_file(self):
        # Инициализация процессоров с содержимым файла
        tree = ET.parse(self.filename)
        root = tree.getroot()
        self.class_processor = ClassProcessor(tree).parse_class_details()
        self.teacher_processor = TeacherProcessor(tree).parse_teachers()
        self.room_processor = RoomProcessor(tree).parse_rooms()
        self.chair_processor = ChairProcessor(tree).parse_chairs()
        self.sched_processor = SchedProcessor(tree).parse_scheds()
        self.plan_processor = PlanProcessor(tree).parse_plans()

    def show_teacher_load(self):
        teacher_load = {}
        for teacher_id, teacher_data in self.teacher_processor.items():
            work_hours = sum(day['hours'] for day in teacher_data['work_hours'])
            total_hours = work_hours + int(teacher_data['method_days'])
            name_parts = [part for part in [teacher_data['surname'], teacher_data['first_name'], teacher_data['second_name']] if part]
            full_name = ' '.join(name_parts)
            teacher_load[teacher_id] = {
                'total_hours': total_hours,
                'name': full_name
            }
        self.teacher_load_form = TeacherLoadForm(teacher_load)
        self.teacher_load_form.show()

    def calculate_and_sort_load_by_department(self):
        # Подсчет рабочих часов для каждого преподавателя
        teacher_load = {}
        for teacher_id, teacher_data in self.teacher_processor.items():
            work_hours = sum(day['hours'] for day in teacher_data['work_hours'])
            total_hours = work_hours + int(teacher_data['method_days'])
            name_parts = [part for part in [teacher_data['surname'], teacher_data['first_name'], teacher_data['second_name']] if part]
            full_name = ' '.join(name_parts)
            teacher_load[teacher_id] = {
                'total_hours': total_hours,
                'name': full_name
            }

        # Агрегация нагрузки по кафедрам с информацией о преподавателях
        department_load = {}
        for teacher_id, load_info in teacher_load.items():
            chair_id = self.teacher_processor[teacher_id]['chair_id']
            if int(chair_id) < 0:
                continue
            chair_name = self.chair_processor.get(int(chair_id))  # Получаем название кафедры по ID
            if chair_name is not None:
                chair_name = chair_name['short_name']
                if chair_name not in department_load:
                    department_load[chair_name] = []
                # Добавление информации о преподавателе в список кафедры
                department_load[chair_name].append({
                    'teacher_name': load_info['name'],
                    'hours': load_info['total_hours']
                })
            else:
                print(f"Ошибка: Не найдена кафедра с ID {chair_id}")
        self.load_table = LoadTable(department_load)
        self.load_table.show()

    # Вывод данных
        for chair_name, teachers in department_load.items():
            print(f"Кафедра {chair_name}:")
            for teacher in teachers:
                print(f"{teacher['teacher_name']}: {teacher['hours']} часов")

    def calc_rooms_load(self):
        room_types = {}
        for room_id, room_data in self.room_processor.items():
            room_type = room_data.get('name')  # Предположим, что тип указан в данных
            if room_type not in room_types:
                room_types[room_type] = []
            room_types[room_type].append(room_data)
        for room_type, rooms in room_types.items():
            print(f"Тип аудитории: {room_type}")
            for room in rooms:
                name = room['name']
                capacity = room['capacity']
                building = room['building']
                chair_id = room['chair_id']
                print(f"Название: {name}, Вместимость: {capacity}, Здание: {building}, Кафедра: {chair_id}")
        return room_types
    
    def get_rooms_load(self):
        room_types = self.calc_rooms_load()
        self.room_load_table = RoomsLoadTable(room_types,self.chair_processor)
        self.room_load_table.show()

    def get_rooms_availability(self):
        room_types = self.calc_rooms_load()
        self.room_availability = RoomAvailabilityChecker(room_types, self.chair_processor)
        self.room_availability.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())

