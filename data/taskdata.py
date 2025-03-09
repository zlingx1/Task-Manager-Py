import json
import uuid

from datetime import datetime

from data.taskprioritytype import TaskPriorityType
from dataclasses import dataclass
from typing import List

@dataclass
class TaskData():
    task_id : uuid.UUID
    task_name : str
    task_priority : TaskPriorityType
    task_date : datetime
    task_attributes : List[str]

    # Convert to JSON
    def to_json(self) -> str:
        return json.dumps({
            "task_id": str(self.task_id), 
            "task_name": self.task_name,
            "task_priority": self.task_priority.value,  
            "task_date" : self.task_date.isoformat(),
            "task_attributes" : self.task_attributes
        })

    # Load from JSON
    @staticmethod
    def from_json(json_str: str) -> "TaskData":
        data = json.loads(json_str)
        return TaskData(
            task_id=uuid.UUID(data["task_id"]),
            task_name=data["task_name"],
            task_priority=TaskPriorityType(data["task_priority"]),
            task_date=datetime.fromisoformat(data["task_date"]),
            task_attributes=data["task_attributes"]
        )