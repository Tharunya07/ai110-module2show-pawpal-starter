from dataclasses import dataclass, field
from typing import List


@dataclass
class Pet:
    name: str
    species: str
    age: int
    notes: str

    def get_info(self) -> str:
        """Return a formatted string summarising the pet's details."""
        pass


class Owner:
    def __init__(self, name: str, available_time_per_day: int, preferences: List[str], pet: Pet):
        self.name = name
        self.available_time_per_day = available_time_per_day
        self.preferences = preferences
        self.pet = pet

    def get_available_time(self) -> int:
        """Return the number of minutes the owner has available per day for pet care."""
        pass


@dataclass
class Task:
    name: str
    duration: int
    priority: str
    category: str
    completed: bool = False

    def is_high_priority(self) -> bool:
        """Return True if this task's priority level is high."""
        pass


class Scheduler:
    def __init__(self, task_list: List[Task], time_budget: int, scheduled_tasks: List[Task]):
        self.task_list = task_list
        self.time_budget = time_budget
        self.scheduled_tasks = scheduled_tasks

    def add_task(self, task: Task) -> None:
        """Add a Task to task_list if it is not already present."""
        pass

    def generate_plan(self) -> List[Task]:
        """Select tasks from task_list that fit within time_budget and populate scheduled_tasks."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the current scheduled_tasks and time usage."""
        pass
