import json

from data.taskdata import TaskData
from window import MainWindow

tasks = None
window = None

def create_window():
    global window
    window = MainWindow()

def contains_task_name(name:str):
    name_lower = name.lower()
    return any(name_lower in task.task_name.lower() for task in tasks)

def load_task(path):
    global tasks
    tasks = []

    with open(path, "r") as f:
        task_list = json.load(f)
        tasks = [TaskData.from_json(task) for task in task_list]

def save_task(path):
    global tasks

    with open(path, "w") as f:
        json.dump([task.to_json() for task in tasks], f, indent = 4)