from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QLineEdit, QStyle
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from data.tasksorttype import TaskSortType
from data.taskprioritytype import TaskPriorityType

from taskview.taskcategory import TaskCategory

class TaskPage(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent_window = parent

        self.sort_on = [TaskSortType.OVERDUE , TaskSortType.SCHEDULED , TaskSortType.TODAY]
        self.priority_on = [TaskPriorityType.NORMAL , TaskPriorityType.HIGH , TaskPriorityType.CRITICAL]

        self.sort_widgets = [None] * len(TaskSortType)
        self.priority_widgets = [None] * len(TaskPriorityType)

        self.page_layout = QVBoxLayout()
        self.page_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.page_layout)

        self.header_layout = QHBoxLayout()
        self.header_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.page_layout.addLayout(self.header_layout)
        
        self.first_content = QHBoxLayout()
        self.first_content.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.second_content = QHBoxLayout()
        self.second_content.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.page_layout.addLayout(self.first_content)
        self.page_layout.addLayout(self.second_content)

        self.__create_header()
        self.__create_sort_header()
        self.__create_categories()
        self.__create_footer()
        
    def __create_header(self):
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search")

        search_icon = self.window().style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
        search_action = QAction(search_icon, "", self.header_layout)
        self.search_bar.addAction(search_action, QLineEdit.ActionPosition.LeadingPosition)
        self.header_layout.addWidget(self.search_bar)

        self.search_bar.returnPressed.connect(self.__search)
        search_action.triggered.connect(self.__search)

    def __search(self):
        self.today_category.update_tasks(self.search_bar.text())
        self.overdue_category.update_tasks(self.search_bar.text())
        self.scheduled_category.update_tasks(self.search_bar.text())

    def __create_sort_header(self):
        self.__create_sort_widget(TaskSortType.TODAY, "Today")
        self.__create_sort_widget(TaskSortType.OVERDUE, "Overdue")
        self.__create_sort_widget(TaskSortType.SCHEDULED, "Scheduled")

        self.__create_priority_widget(TaskPriorityType.NORMAL, "Normal")
        self.__create_priority_widget(TaskPriorityType.HIGH, "High")
        self.__create_priority_widget(TaskPriorityType.CRITICAL, "Critical")

    def __create_categories(self):
        category_layout = QVBoxLayout()
        category_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        category_widget = QWidget()
        category_widget.setLayout(category_layout)

        category_area = QScrollArea()
        category_area.setWidgetResizable(True)
        category_area.setWidget(category_widget)

        self.today_category = TaskCategory(TaskSortType.TODAY.name, self)
        self.overdue_category = TaskCategory(TaskSortType.OVERDUE.name, self)
        self.scheduled_category = TaskCategory(TaskSortType.SCHEDULED.name, self)
        category_layout.addLayout(self.today_category)
        category_layout.addLayout(self.overdue_category)
        category_layout.addLayout(self.scheduled_category)

        self.page_layout.addWidget(category_area)

    def __create_footer(self):
        footer_layout = QHBoxLayout()

        new_task_button = QPushButton()
        new_task_button.clicked.connect(lambda: self.parent_window.switch_page(2))
        new_task_button.setText("New Task")

        footer_layout.addWidget(new_task_button)
        self.page_layout.addLayout(footer_layout)

    def __create_sort_widget(self, sort_type : TaskSortType, name:str):
        self.sort_widgets[sort_type.value] = QPushButton(name)
        self.sort_widgets[sort_type.value].clicked.connect(lambda: self.__filter_sort_selected(sort_type))
        self.sort_widgets[sort_type.value].setStyleSheet("""
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
        stop:0 gray, stop:1 lightblue);
        """)
        self.first_content.addWidget(self.sort_widgets[sort_type.value])

    def __create_priority_widget(self, sort_type : TaskPriorityType, name:str):
        self.priority_widgets[sort_type.value] = QPushButton(name)
        self.priority_widgets[sort_type.value].clicked.connect(lambda: self.__filter_priority_selected(sort_type))
        self.priority_widgets[sort_type.value].setStyleSheet("""
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
        stop:0 gray, stop:1 lightblue);
        """)
        self.second_content.addWidget(self.priority_widgets[sort_type.value])

    def __filter_sort_selected(self, sort_type : TaskSortType):
        if sort_type in self.sort_on:
            self.disable_sort_type(sort_type)
        else:
            self.enable_sort_type(sort_type)
            
        match sort_type:
            case TaskSortType.TODAY: self.today_category.set_expanded_state(sort_type in self.sort_on) 
            case TaskSortType.OVERDUE: self.overdue_category.set_expanded_state(sort_type in self.sort_on)
            case TaskSortType.SCHEDULED: self.scheduled_category.set_expanded_state(sort_type in self.sort_on)

    def __filter_priority_selected(self, sort_type : TaskPriorityType):
        if sort_type in self.priority_on:
            self.priority_on.remove(sort_type)        
            self.priority_widgets[sort_type.value].setStyleSheet("""
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
            stop:0 gray, stop:1 black);
            """)
        else:
            self.priority_on.append(sort_type)        
            self.priority_widgets[sort_type.value].setStyleSheet("""
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
            stop:0 gray, stop:1 lightblue);
            """)

    def disable_sort_type(self, sort_type : TaskSortType):
        if sort_type not in self.sort_on:
            return

        self.sort_on.remove(sort_type)        
        self.sort_widgets[sort_type.value].setStyleSheet("""
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
        stop:0 gray, stop:1 black);
        """)

    def enable_sort_type(self, sort_type : TaskSortType):
        if sort_type in self.sort_on:
            return

        self.sort_on.append(sort_type)        
        self.sort_widgets[sort_type.value].setStyleSheet("""
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
        stop:0 gray, stop:1 lightblue);
        """)

    def update_categories(self):
        self.today_category.update_tasks()
        self.overdue_category.update_tasks()
        self.scheduled_category.update_tasks()