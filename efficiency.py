import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel

class EfficiencyForm(QWidget):
    def __init__(self, items, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout(self)

        self.comboBox = QComboBox()
        self.comboBox.addItems(items)
        layout.addWidget(self.comboBox)

        self.calcButton = QPushButton("Рассчитать")
        self.calcButton.clicked.connect(self.calculate_efficiency)
        layout.addWidget(self.calcButton)

        self.resultLabel = QLabel("Эффективность: ")
        layout.addWidget(self.resultLabel)

    def calculate_efficiency(self):
        eff = round(random.uniform(0, 20), 2)
        self.resultLabel.setText(f"Эффективность: {eff}")