from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QScrollArea, QPushButton, QStyle,  QApplication
from PyQt6.QtCore import Qt

from data.taskdata import TaskData
from taskview.taskpanel import TaskPanel

from data.tasksorttype import TaskSortType

from datetime import datetime

import manager

class TaskCategory(QVBoxLayout):
    def __init__(self,  category_id : str, parent):
        super().__init__()

        self.parent_page = parent
        self.category_id = category_id
        self.expanded = True
        
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        header_layout = QHBoxLayout()

        title_label = QLabel(category_id)
        title_label.setStyleSheet("""
        background-color: #101010;
        color: white;    
        padding: 5px;      
        border-radius: 10px; 
        font-weight: bold;
        """)

        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedWidth(30)
        self.toggle_btn.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))  
        self.toggle_btn.clicked.connect(lambda: self.__toggle_view(not self.expanded))

        header_layout.addWidget(title_label)
        header_layout.addWidget(self.toggle_btn)

        self.addLayout(header_layout)

        self.task_layout = QVBoxLayout()
        self.task_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        attribute_widget = QWidget()
        attribute_widget.setLayout(self.task_layout)
        self.attribute_area = QScrollArea()
        self.attribute_area.setWidgetResizable(True)
        self.attribute_area.setWidget(attribute_widget)

        self.addWidget(self.attribute_area)

        self.update_tasks()

    def update_tasks(self, filter : str = ""):
        for index in reversed(range(self.task_layout.count())):
            widget = self.task_layout.itemAt(index).widget()
            self.task_layout.removeWidget(widget)
            widget.setParent(None)

        sorted_tasks = [task for task in manager.tasks if self.__filter_task(task, filter)]

        sorted_tasks = sorted(sorted_tasks, key=lambda task: task.task_priority.value)

        for task in sorted_tasks:
            self.add_task(task)

        if len(sorted_tasks) == 0:
            self.__toggle_view(False)

    def __filter_task(self, task : TaskData, filter : str = "") -> bool:
        task_name = task.task_name.lower()

        if filter != "" and filter not in task_name:
            return False

        today = datetime.now().date()
        due = task.task_date.date()

        if self.category_id == TaskSortType.OVERDUE.name:
            return due < today
        elif self.category_id == TaskSortType.SCHEDULED.name:
            return due > today
        else:
            return due == today
        
    def add_task(self, data : TaskData):
        if self.__filter_task(data) == False:
            return

        task_panel = TaskPanel(data)
        self.task_layout.addWidget(task_panel)

    def __toggle_view(self, state:bool):
        self.set_expanded_state(state)
        
        if self.expanded == False:
            self.parent_page.disable_sort_type(TaskSortType[self.category_id])
        else:
            self.parent_page.enable_sort_type(TaskSortType[self.category_id])
        
    def set_expanded_state(self, state: bool):
        self.expanded = state

        self.attribute_area.setVisible(self.expanded)

        icon = QStyle.StandardPixmap.SP_ArrowDown if self.expanded else QStyle.StandardPixmap.SP_ArrowRight
        self.toggle_btn.setIcon(QApplication.style().standardIcon(icon))

