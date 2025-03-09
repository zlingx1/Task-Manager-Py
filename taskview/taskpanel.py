from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

from PyQt6.QtCore import Qt

from data.taskdata import TaskData

class TaskPanel(QWidget):
    def __init__(self, data : TaskData):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.main_layout)

        self.name_widget = QLabel(data.task_name)

        self.main_layout.addWidget(self.name_widget)

        self.setStyleSheet("background: black")



        