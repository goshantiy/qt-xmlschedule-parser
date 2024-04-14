import os
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt


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

        # Определяем максимальное количество преподавателей в отделениях
        max_teachers = max(len(loads) for loads in self.department_load.values())

        # Устанавливаем количество столбцов (2 для названий + 2 для каждого преподавателя)
        self.tableWidget.setColumnCount(2 + 2 * max_teachers)

        # Устанавливаем заголовки таблицы
        headers = ['Кафедра', 'Количество преподавателей']
        for i in range(max_teachers):
            headers.extend([f"Преподаватель {i+1}", f"Часы {i+1}"])
        self.tableWidget.setHorizontalHeaderLabels(headers)

        # Установка количества строк
        self.tableWidget.setRowCount(len(self.department_load))

        # Заполнение таблицы
        for i, (department, loads) in enumerate(self.department_load.items()):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(department))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(len(loads))))

            for j, load in enumerate(loads):
                col_index = 2 + 2 * j  # Находим начальный индекс столбца для текущего преподавателя
                self.tableWidget.setItem(i, col_index, QTableWidgetItem(load['teacher_name']))
                self.tableWidget.setItem(i, col_index + 1, QTableWidgetItem(str(load['hours'])))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)  # Растягивание последней колонки для заполнения пространства


    def export_to_excel(self):
        # Создание DataFrame из словаря
        data = []
        for department, loads in self.department_load.items():
            for load in loads:
                data.append([department, f"{load['teacher_name']} ({load['hours']} часов)"])

        df = pd.DataFrame(data, columns=['Кафедра', 'Нагрузка'])

        # Имя файла
        filename = 'нагрузка_по_кафедрам.xlsx'
        
        # Экспорт в Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        print("Данные успешно экспортированы в Excel")
        
        # Попытка открыть файл
        try:
            if os.name == 'nt':  # Для Windows
                os.startfile(filename)
            elif os.name == 'posix':  # Для macOS и Linux
                opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                os.system(opener + ' ' + filename)
        except Exception as e:
            print(f"Не удалось открыть файл: {e}")

