from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QScrollArea
from PyQt6.QtCore import Qt

from data.taskdata import TaskData
from taskview.taskpanel import TaskPanel

from data.tasksorttype import TaskSortType
from data.taskprioritytype import TaskPriorityType

from datetime import datetime
from typing import List

import manager

class TaskCategory(QVBoxLayout):
    def __init__(self,  category_id : str):
        super().__init__()

        self.category_id = category_id
        self.task_panels = []

        self.setAlignment(Qt.AlignmentFlag.AlignTop)

        title_label = QLabel(category_id)
        title_label.setStyleSheet("""
        background-color: black;
        color: white;    
        padding: 5px;      
        border-radius: 10px; 
        font-weight: bold;
        """)

        self.addWidget(title_label)

        self.attribute_layout = QVBoxLayout()
        self.attribute_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        attribute_widget = QWidget()
        attribute_widget.setLayout(self.attribute_layout)
        attribute_area = QScrollArea()
        attribute_area.setWidgetResizable(True)
        attribute_area.setWidget(attribute_widget)

        self.addWidget(attribute_area)

        self.__create_view()

    def __create_view(self):
        sorted_tasks = [task for task in manager.tasks if self.__filter_task(task)]
        sorted_tasks = sorted(sorted_tasks, key=lambda task: task.task_priority.value)

        for task in sorted_tasks:
            self.add_task(task)

    def __filter_task(self, task : TaskData) -> bool:
        today = datetime.now()

        print(f"{self.category_id} {today} {task.task_date}")

        if self.category_id == TaskSortType.OVERDUE:
            return task.task_date > today
        elif self.category_id == TaskSortType.SCHEDULED:
            return task.task_date < today
        else:
            return True
        
    def add_task(self, data : TaskData):
        if self.__filter_task(data) == False:
            return

        task_panel = TaskPanel(data)
        self.attribute_layout.addWidget(task_panel)
