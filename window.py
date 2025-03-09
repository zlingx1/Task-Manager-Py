from PyQt6.QtWidgets import QStackedWidget, QPushButton, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt


from pages.taskpage import TaskPage
from pages.newtaskpage import NewTaskPage
from pages.settingspage import SettingsPage

class MainWindow():
    TASK_PAGE = 0
    SETTING_PAGE = 1
    NEW_TASK_PAGE = 2

    def __init__(self):

        self.window = QMainWindow()

        self.main_widget = QWidget()
        self.window.setCentralWidget(self.main_widget)

        self.task_page = TaskPage(self)
        self.settings_page = SettingsPage() 
        self.new_task_page = NewTaskPage(self)

        self.__create_window()

    def __create_nav_btn(self, title:str, handler):
        button = QPushButton(title)
        button.setStyleSheet("""
            background-color: #555;
            color: white;
            font-size: 16px;
            padding: 10px;
            border: none;""")
        
        button.clicked.connect(handler)
        return button

    def __create_window(self):
        self.window.setWindowTitle("Tasking Manager")
        self.window.setGeometry(0, 0, 800, 600)

        main_layout = QHBoxLayout(self.main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        sidebar = QWidget()
        sidebar.setContentsMargins(0, 0, 0, 0)
        sidebar.setFixedWidth(100)
        sidebar.setStyleSheet("background-color: #333;")  

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        sidebar_layout.addWidget(self.__create_nav_btn("Task", lambda: self.switch_page(MainWindow.TASK_PAGE)))
        sidebar_layout.addWidget(self.__create_nav_btn("Settings", lambda: self.switch_page(MainWindow.SETTING_PAGE)))

        sidebar.setLayout(sidebar_layout)

        self.pages = QStackedWidget()

        self.pages.addWidget(self.task_page)
        self.pages.addWidget(self.settings_page)
        self.pages.addWidget(self.new_task_page)
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages, 1)

    def switch_page(self, page_index):
        self.pages.setCurrentIndex(page_index)

    def show(self):
        self.window.show()
