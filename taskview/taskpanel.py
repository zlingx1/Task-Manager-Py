from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QPushButton, QLabel, QSizePolicy

from PyQt6.QtCore import Qt

from data.taskdata import TaskData

import manager

class TaskPanel(QWidget):
    def __init__(self, data : TaskData):
        super().__init__()
        self.task_data = data

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.attribute_status_widgets = []

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.header_layout = QHBoxLayout()
        self.header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.name_widget = QPushButton(data.task_name)
        self.name_widget.clicked.connect(lambda: manager.window.open_edit_task_page(self.task_data))
        self.name_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.header_layout.addWidget(self.name_widget)

        self.status_widget = QCheckBox()
        self.status_widget.setChecked(data.task_status)
        self.status_widget.stateChanged.connect(self.__task_checked)
        self.header_layout.addWidget(self.status_widget)
        
        self.main_layout.addLayout(self.header_layout)

        self.__create_attributes()

        self.setLayout(self.main_layout)

    def __create_attributes(self):
        for key, value in self.task_data.task_attributes.items():
            self.__create_attribute(key, value)

    def __create_attribute(self, key:str, status:bool):
        attribute_layout = QHBoxLayout()
        attribute_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        name_widget = QLabel(key)
        name_widget.setMaximumWidth(int(self.width() * 0.925))
        name_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        attribute_layout.addWidget(name_widget)

        name_widget.setStyleSheet("""
        background-color: gray;
        color: white;       
        padding: 2px;      
        border-radius: 5px; 
        font-weight: bold;
        """)

        status_widget = QCheckBox()
        status_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        status_widget.setChecked(status)
        status_widget.stateChanged.connect(lambda: self.__attribute_checked(key, status))
        attribute_layout.addWidget(status_widget)

        self.attribute_status_widgets.append(status_widget)

        self.main_layout.addLayout(attribute_layout)

    def __task_checked(self, state):
        self.task_data.task_status = state == 2

        for widget in self.attribute_status_widgets:
            widget.setChecked(self.task_data.task_status)
        
    def __attribute_checked(self, attribute, status):
        self.task_data.task_attributes[attribute] = status        