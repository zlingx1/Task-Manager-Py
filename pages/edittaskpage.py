from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QLineEdit, QComboBox, QDateEdit
from PyQt6.QtCore import Qt, QDate

import uuid

from data.taskprioritytype import TaskPriorityType
from data.taskdata import TaskData

from datetime import datetime

import manager

class EditTaskPage(QWidget):
    def __init__(self, task_data : TaskData):
        super().__init__()
        self.task_data : TaskData = task_data

        self.page_layout = QVBoxLayout()

        self.attributes = []

        self.title_field = QLineEdit()
        self.title_field.setText(self.task_data.task_name)
        self.title_field.setStyleSheet("font-size: 18px; padding: 6px;") 
        self.page_layout.addWidget(self.title_field)

        status_layout = QHBoxLayout()

        self.priority_combo = QComboBox()
        for priority in TaskPriorityType:
            self.priority_combo.addItem(priority.name)
        self.priority_combo.setCurrentText(self.task_data.task_priority.name)

        status_layout.addWidget(self.priority_combo)

        self.status_date = QDateEdit()
        self.status_date.setCalendarPopup(True)
        self.status_date.setDate(QDate(self.task_data.task_date.year, self.task_data.task_date.month, self.task_data.task_date.day))

        status_layout.addWidget(self.status_date)

        self.page_layout.addLayout(status_layout)

        self.attribute_layout = QVBoxLayout()
        self.attribute_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        attribute_widget = QWidget()
        attribute_widget.setLayout(self.attribute_layout)
        attribute_area = QScrollArea()
        attribute_area.setWidgetResizable(True)
        attribute_area.setWidget(attribute_widget)

        self.page_layout.addWidget(attribute_area)

        add_attr_button = QPushButton("New Attribute")
        add_attr_button.clicked.connect(lambda: self.__add_new_attribute())
        self.page_layout.addWidget(add_attr_button)

        self.submit_button = QPushButton("Update Task")
        self.submit_button.setStyleSheet("font-size: 18px; padding: 6px;") 
        self.submit_button.clicked.connect(self.submit_task)

        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        footer_layout.addWidget(self.submit_button)

        self.page_layout.addLayout(footer_layout)

        self.setLayout(self.page_layout)

        for attribute in task_data.task_attributes:
            self.__add_new_attribute(attribute)

    def __add_new_attribute(self, text:str = ""):
        attribute_label = QLineEdit()

        if text == "":
            attribute_label.setPlaceholderText(text)
        else:
            attribute_label.setText(text)
        
        self.attributes.append(attribute_label)

        self.attribute_layout.addWidget(attribute_label)

    def submit_task(self):
        manager.tasks.remove(self.task_data)

        title = self.title_field.text()
        attributes = {label.text(): False for label in self.attributes}
        date = self.status_date.date().toPyDate()

        task_data = TaskData(
            uuid.uuid4(),
            title,
            TaskPriorityType[self.priority_combo.currentText()],
            datetime(date.year, date.month, date.day),
            False,
            attributes)
        
        manager.tasks.append(task_data)
        
        self.task_data = None

        manager.window.switch_page(0)
        manager.window.remove_page(self)
        
        self.setParent(None)