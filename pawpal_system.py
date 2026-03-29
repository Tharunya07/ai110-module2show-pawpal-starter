from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Pet:
    name: str
    species: str
    age: int
    notes: str
    tasks: List["Task"] = field(default_factory=list)

    def get_info(self) -> str:
        """Return a formatted string summarising the pet's details."""
        return f"{self.name} ({self.species}, age {self.age}) — {self.notes}"


class Owner:
    def __init__(self, name: str, available_time_per_day: int, preferences: List[str], pets: List[Pet]):
        """Initialise an Owner with their name, daily time budget, preferences, and list of pets."""
        self.name = name
        self.available_time_per_day = available_time_per_day
        self.preferences = preferences
        self.pets = pets

    def get_available_time(self) -> int:
        """Return the number of minutes the owner has available per day for pet care."""
        return self.available_time_per_day

    def get_all_tasks(self, task_list: List["Task"]) -> List["Task"]:
        """Return all tasks from task_list whose pet belongs to this owner."""
        owner_pets = set(id(pet) for pet in self.pets)
        return [task for task in task_list if id(task.pet) in owner_pets]


@dataclass
class Task:
    name: str
    duration: int
    priority: Priority
    category: str
    pet: Pet
    completed: bool = False

    def __eq__(self, other: object) -> bool:
        """Return True if two tasks share the same name and pet."""
        if not isinstance(other, Task):
            return NotImplemented
        return self.name == other.name and self.pet == other.pet

    def __hash__(self):
        """Return a hash based on the task name and pet name."""
        return hash((self.name, self.pet.name))

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_high_priority(self) -> bool:
        """Return True if this task's priority level is high."""
        return self.priority == Priority.HIGH


class Scheduler:
    def __init__(self, task_list: List[Task], owner: Owner):
        """Initialise the Scheduler with a task list and an owner whose time budget drives planning."""
        self.task_list = task_list
        self.owner = owner
        self.scheduled_tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a Task to task_list if it is not already present."""
        if task not in self.task_list:
            self.task_list.append(task)

    def generate_plan(self) -> List[Task]:
        """Select tasks from task_list that fit within owner.available_time_per_day and populate scheduled_tasks."""
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        all_tasks = self.owner.get_all_tasks(self.task_list)
        sorted_tasks = sorted(all_tasks, key=lambda t: priority_order[t.priority])

        time_remaining = self.owner.get_available_time()
        self.scheduled_tasks = []

        for task in sorted_tasks:
            if task.duration <= time_remaining:
                self.scheduled_tasks.append(task)
                time_remaining -= task.duration

        return self.scheduled_tasks

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the current scheduled_tasks and time usage."""
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        all_tasks = self.owner.get_all_tasks(self.task_list)
        sorted_tasks = sorted(all_tasks, key=lambda t: priority_order[t.priority])
        scheduled_set = set(id(t) for t in self.scheduled_tasks)

        lines = []
        time_used = sum(t.duration for t in self.scheduled_tasks)
        time_budget = self.owner.get_available_time()

        lines.append(f"Daily plan for {self.owner.name} ({time_used}/{time_budget} min used):\n")

        lines.append("Scheduled:")
        for task in self.scheduled_tasks:
            lines.append(
                f"  - {task.name} for {task.pet.name} | {task.priority.value} priority | {task.duration} min"
            )

        skipped = [t for t in sorted_tasks if id(t) not in scheduled_set]
        if skipped:
            lines.append("\nSkipped (time ran out):")
            for task in skipped:
                lines.append(
                    f"  - {task.name} for {task.pet.name} | {task.priority.value} priority | {task.duration} min needed"
                )

        return "\n".join(lines)
