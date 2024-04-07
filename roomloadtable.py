import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QFileDialog

class RoomsLoadTable(QWidget):
    def __init__(self, room_types, chair_processor):
        super().__init__()
        self.room_types = room_types
        self.chair_processor = chair_processor  # Словарь для преобразования chair_id в названия
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Аудитории')
        self.layout = QVBoxLayout(self)

        self.tableWidget = QTableWidget()
        self.layout.addWidget(self.tableWidget)

        self.exportButton = QPushButton('Экспорт в Excel')
        self.exportButton.clicked.connect(self.export_to_excel)

        self.layout.addWidget(self.exportButton)

        self.populate_table()

    def populate_table(self):
        rows = sum(len(rooms) for rooms in self.room_types.values())
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(6)  # Добавлен столбец для нагрузки
        self.tableWidget.setHorizontalHeaderLabels(['Тип аудитории', 'Название', 'Вместимость', 'Здание', 'Кафедра', 'Нагрузка(ч)'])

        current_row = 0
        for room_type, rooms in self.room_types.items():
            for room in rooms:
                chair_name = self.chair_processor.get(int(room['chair_id']), {'short_name': 'Неизвестно'})['short_name']  # Получаем название кафедры по ID
                # Рассчитываем нагрузку по рабочим часам
                work_hours_load = sum(sum(int(bit) for bit in day) for week in room['work_hours'].values() for day in week.values())
                
                self.tableWidget.setItem(current_row, 0, QTableWidgetItem(room_type))
                self.tableWidget.setItem(current_row, 1, QTableWidgetItem(room['name']))
                self.tableWidget.setItem(current_row, 2, QTableWidgetItem(room['capacity']))
                self.tableWidget.setItem(current_row, 3, QTableWidgetItem(room['building']))
                self.tableWidget.setItem(current_row, 4, QTableWidgetItem(chair_name))  # Используем название кафедры
                self.tableWidget.setItem(current_row, 5, QTableWidgetItem(str(work_hours_load)))  # Нагрузка
                current_row += 1

        self.tableWidget.resizeColumnsToContents()

    def export_to_excel(self):
        filename, _ = os.path.splitext(os.path.basename(__file__))
        filepath, _ = QFileDialog.getSaveFileName(self, "Сохранить как", filename, "Excel Files (*.xlsx)")

        if filepath:
            df = self.get_table_data_as_dataframe()
            df.to_excel(filepath, index=False)

    def get_table_data_as_dataframe(self):
        columns = ['Тип аудитории', 'Название', 'Вместимость', 'Здание', 'Кафедра', 'Нагрузка']
        data = []
        for row in range(self.tableWidget.rowCount()):
            row_data = []
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
            data.append(row_data)
        return pd.DataFrame(data, columns=columns)
