import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton

class LoadTable(QWidget):
    def __init__(self, department_load):
        super().__init__()
        self.title = 'Нагрузка по кафедрам'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 300
        self.department_load = department_load

        self.initUI()
        self.export_to_excel_button = QPushButton("Экспорт в Excel")
        self.export_to_excel_button.clicked.connect(self.export_to_excel)
        self.layout.addWidget(self.export_to_excel_button)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Создание таблицы
        self.createTable()

        # Добавление таблицы в layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

    def createTable(self):
        self.tableWidget = QTableWidget()

        # Установка количества колонок
        self.tableWidget.setColumnCount(2)

        # Установка заголовков таблицы
        self.tableWidget.setHorizontalHeaderLabels(['Кафедра', 'Нагрузка'])

        # Установка количества строк
        self.tableWidget.setRowCount(len(self.department_load))

        # Заполнение таблицы элементами
        for i, (department, load) in enumerate(self.department_load.items()):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(department))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(load)))

        self.tableWidget.resizeColumnsToContents()
    def export_to_excel(self):
        df = pd.DataFrame(list(self.department_load.items()), columns=['Кафедра', 'Нагрузка'])
        filename = 'нагрузка_по_кафедрам.xlsx'
        df.to_excel(filename, index=False, engine='openpyxl')
        print("Данные успешно экспортированы в Excel")
        try:
            if os.name == 'nt':  # Для Windows
                os.startfile(filename)
            elif os.name == 'posix':  # Для macOS и Linux
                opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                os.system(opener + ' ' + filename)
        except Exception as e:
            print(f"Не удалось открыть файл: {e}")
