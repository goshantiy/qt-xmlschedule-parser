from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDateEdit
from PyQt5.QtCore import QDate
import sys
from roomscheduler import RoomScheduler  # Импорт класса RoomScheduler из вашего модуля roomscheduler

class RoomAvailabilityChecker(QWidget):
    def __init__(self, room_types, chair_processor):
        super().__init__()
        self.room_types = room_types
        self.chair_processor = chair_processor
        self.scheduler = RoomScheduler(room_types)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Проверка доступности аудиторий')
        self.layout = QVBoxLayout(self)

        self.roomTypeComboBox = QComboBox()
        self.roomTypeComboBox.addItems(['Все'] + list(self.room_types))
        self.layout.addWidget(self.roomTypeComboBox)

        self.dateEdit = QDateEdit()
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QDate.currentDate())
        self.layout.addWidget(self.dateEdit)

        self.pairPositionLineEdit = QLineEdit()
        self.pairPositionLineEdit.setPlaceholderText('Позиция пары (1-8)')
        self.layout.addWidget(self.pairPositionLineEdit)

        self.checkAvailabilityButton = QPushButton('Проверить доступность')
        self.checkAvailabilityButton.clicked.connect(self.check_availability)
        self.layout.addWidget(self.checkAvailabilityButton)

        self.resultsTable = QTableWidget()
        self.layout.addWidget(self.resultsTable)

    def check_availability(self):
        self.resultsTable.clear()
        self.resultsTable.setRowCount(0)
        self.resultsTable.setColumnCount(5)
        self.resultsTable.setHorizontalHeaderLabels(['Тип', 'Название', 'Вместимость', 'Здание', 'Кафедра'])

        room_type = self.roomTypeComboBox.currentText()
        date = self.dateEdit.date().toString('dd.MM.yyyy')
        pair_position = int(self.pairPositionLineEdit.text())

        filtered_rooms = []

        for room_id, room_data_list in self.room_types.items():
            # Получаем информацию об аудитории из списка
            room_data = room_data_list[0]
            if room_type != 'Все' and room_data.get('type') != room_type:
                continue

            # Проверяем, занята ли аудитория в указанную дату и пару
            if room_id not in self.scheduler.schedule or \
               date not in self.scheduler.schedule[room_id] or \
               pair_position not in self.scheduler.schedule[room_id][date]:
                # Если аудитория свободна в указанную дату и время, добавляем в фильтрованный список
                filtered_rooms.append(room_data)

        # Заполняем таблицу фильтрованными данными
        self.resultsTable.setRowCount(len(filtered_rooms))

        for row, room in enumerate(filtered_rooms):
            chair_name = self.chair_processor.get(int(room['chair_id']), {'short_name': 'Неизвестно'})['short_name']
            self.resultsTable.setItem(row, 0, QTableWidgetItem(room.get('type')))
            self.resultsTable.setItem(row, 1, QTableWidgetItem(room.get('name')))
            self.resultsTable.setItem(row, 2, QTableWidgetItem(room.get('capacity')))
            self.resultsTable.setItem(row, 3, QTableWidgetItem(room.get('building')))
            self.resultsTable.setItem(row, 4, QTableWidgetItem(chair_name))

        self.resultsTable.resizeColumnsToContents()
