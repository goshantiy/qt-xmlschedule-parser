from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class TeacherLoadForm(QWidget):
    def __init__(self, teacher_load):
        super().__init__()
        self.setWindowTitle("Нагрузка преподавателей")
        self.setGeometry(100, 100, 600, 400)  # Можно настроить размеры окна

        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Номер, ФИО, Количество часов
        self.table.setHorizontalHeaderLabels(["Номер", "ФИО", "Количество часов"])
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_data(teacher_load)

    def load_data(self, teacher_load):
        # Отображение данных о преподавателях
        self.table.setRowCount(len(teacher_load))
        for index, (teacher_id, data) in enumerate(teacher_load.items()):
            self.table.setItem(index, 0, QTableWidgetItem(str(teacher_id)))
            self.table.setItem(index, 1, QTableWidgetItem(data['name']))
            self.table.setItem(index, 2, QTableWidgetItem(str(data['total_hours'])))
