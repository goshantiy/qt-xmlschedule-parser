from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox
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
        selected_date = self.dateEdit.date().toString('dd.MM.yyyy')  # Получаем выбранную дату
        hour = int(self.pairPositionLineEdit.text()) if self.pairPositionLineEdit.text().isdigit() else None  # Выбранный час (0-23)

        if hour is None or not 0 <= hour <= 8:
            QMessageBox.warning(self, 'Ошибка', 'Некорректный ввод. Введите число от 0 до 8.')
            return

        filtered_rooms = []

        for room_id, room_schedule in self.scheduler.schedule.items():
            # Проверяем доступность аудитории в указанную дату и время
            if selected_date in room_schedule and hour in room_schedule[selected_date]:
                # Аудитория доступна в указанное время, добавляем в фильтрованный список
                filtered_rooms.append(room_id)

        # Заполняем таблицу фильтрованными данными
        self.resultsTable.setRowCount(len(filtered_rooms))

        for row, room_id in enumerate(filtered_rooms):
            room_data = self.room_types[room_id][0]  # Получаем информацию об аудитории
            chair_name = self.chair_processor.get(int(room_data['chair_id']), {'short_name': 'Неизвестно'})['short_name']
            self.resultsTable.setItem(row, 0, QTableWidgetItem(room_data.get('type')))
            self.resultsTable.setItem(row, 1, QTableWidgetItem(room_data.get('name')))
            self.resultsTable.setItem(row, 2, QTableWidgetItem(room_data.get('capacity')))
            self.resultsTable.setItem(row, 3, QTableWidgetItem(room_data.get('building')))
            self.resultsTable.setItem(row, 4, QTableWidgetItem(chair_name))

        self.resultsTable.resizeColumnsToContents()

