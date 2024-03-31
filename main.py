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

        self.type_selector = QComboBox()  # Для выбора типа элементов
        self.types = ["Classes", "Subjects", "Rooms", "Chairs", "Teachers", "Scheds", "Study Types"]
        self.type_selector.addItems(self.types)
        self.layout.addWidget(self.type_selector)

        self.item_selector = QComboBox()  # Для выбора конкретного элемента
        self.layout.addWidget(self.item_selector)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Tag", "Text", "Attribute"])
        self.layout.addWidget(self.tree_widget)

        self.setWindowTitle("XML Viewer")
        self.filename = ""

        self.type_selector.currentIndexChanged.connect(self.populate_item_selector)  # Заполнить при смене типа
        self.item_selector.currentIndexChanged.connect(self.parse_selected_item)

    def select_file(self):
        options = QFileDialog.Options()
        self.filename, _ = QFileDialog.getOpenFileName(self, "Выбрать XML файл", "", "XML Files (*.xml)", options=options)
        if self.filename:
            self.file_selected_label.setText(f"Выбранный файл: {self.filename}")
            self.populate_item_selector()  # Обновляем список элементов после выбора файла

    def populate_item_selector(self):
        self.item_selector.clear()  # Очищаем список элементов перед заполнением
        if not self.filename:
            return  # Выход, если файл не выбран

        selected_type = self.type_selector.currentText()
        processor = None  # Инициализируем переменную processor

        if selected_type == "Classes":
            processor = ClassProcessor(self.filename)
        elif selected_type == "Subjects":
            processor = SubjectProcessor(self.filename)
        elif selected_type == "Rooms":
            processor = RoomProcessor(self.filename)
        elif selected_type == "Chairs":
            processor = ChairProcessor(self.filename)
        elif selected_type == "Teachers":
            processor = TeacherProcessor(self.filename)
        elif selected_type == "Scheds":
            processor = SchedProcessor(self.filename)
        elif selected_type == "Study Types":
            processor = StudyTypeProcessor(self.filename)
        else:
            return  # Необходимый обработчик не найден

        # Теперь, когда у нас есть правильный процессор, можем получить имена элементов
        if processor:
            # В зависимости от типа процессора, вызываем нужный метод

            item_names = processor.get_names()  # Вызываем метод для получения имен

            for name in item_names:
                self.item_selector.addItem(name)

    def parse_selected_item(self):
        # Этот метод можно реализовать для заполнения tree_widget данными выбранного элемента
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())

