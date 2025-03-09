
import sys

from PyQt6.QtWidgets import QApplication

import manager

task_path:str = "Task.json"

def main():
    manager.load_task(task_path)

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(lambda: manager.save_task(task_path))
    
    manager.create_window()

    manager.window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()