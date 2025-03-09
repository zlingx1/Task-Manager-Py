
import sys

from PyQt6.QtWidgets import QApplication

from window import MainWindow

import manager


task_path:str = "Task.json"

def main():
    manager.load_task(task_path)

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(lambda: manager.save_task(task_path))
    win = MainWindow()

    win.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()