import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QComboBox, QVBoxLayout, QWidget, QPushButton, QFileDialog, QHBoxLayout, QLabel
import xml.etree.ElementTree as ET
from xmlprocessing import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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

        # Добавляем макет и виджеты для расчета нагрузки
        self.calc_load_layout = QHBoxLayout()  # Создаем новый горизонтальный макет для элементов управления расчетом нагрузки
        self.layout.addLayout(self.calc_load_layout)  # Добавляем новый макет в основной вертикальный макет

        self.calc_load_label = QLabel("Расчет нагрузки:")  # Метка для кнопки расчета
        self.calc_load_button = QPushButton("Рассчитать нагрузку")  # Кнопка для инициации расчета
        self.calc_load_button.clicked.connect(self.calculate_and_sort_load_by_department)  # Подключаем событие клика к методу расчета
        self.calc_load_layout.addWidget(self.calc_load_label)  # Добавляем метку в макет
        self.calc_load_layout.addWidget(self.calc_load_button)  # Добавляем кнопку в макет

        self.setWindowTitle("XML Viewer")
        self.filename = ""

    def select_file(self):
        options = QFileDialog.Options()
        self.filename, _ = QFileDialog.getOpenFileName(self, "Выбрать XML файл", "", "XML Files (*.xml)", options=options)
        if self.filename:
            self.file_selected_label.setText(f"Выбранный файл: {self.filename}")
            self.parse_file()  
            
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

    def calculate_and_sort_load_by_department(self):
        # Подсчет рабочих часов для каждого преподавателя
        teacher_load = {}
        for teacher in self.teacher_processor:
            work_hours = sum(bin(int(day)).count('1') for day in teacher['work_hours'])
            method_days = int(teacher['method_days'])
            total_hours = work_hours + method_days
            teacher_load[teacher['id']] = total_hours

        # Агрегация нагрузки по кафедрам
        department_load = {}
        for teacher_id, load in teacher_load.items():
            department_id = self.teacher_processor.teachers[teacher_id]['department_id']
            if department_id not in department_load:
                department_load[department_id] = load
            else:
                department_load[department_id] += load

        # Сортировка и вывод данных
        # Здесь можно добавить логику сортировки по убыванию, возрастанию или алфавиту
        # Для демонстрации просто выведем данные без сортировки
        for dept_id, load in department_load.items():
            print(f"Кафедра {dept_id}: {load} часов")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())

