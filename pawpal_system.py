from dataclasses import dataclass, field
from datetime import date
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
    recurrence: str | None = None
    last_scheduled: date | None = None

    def __eq__(self, other: object) -> bool:
        """Return True if two tasks share the same name and pet."""
        if not isinstance(other, Task):
            return NotImplemented
        return self.name == other.name and self.pet == other.pet

    def __hash__(self):
        """Return a hash based on the task name and pet name."""
        return hash((self.name, self.pet.name))

    def is_due(self, today: date) -> bool:
        """Return True if this task should be scheduled on the given date.
        Non-recurring and daily tasks are always due; weekly tasks are due
        if they have never been scheduled or were last scheduled 7+ days ago."""
        if self.recurrence is None or self.recurrence == "daily":
            return True
        if self.recurrence == "weekly":
            return self.last_scheduled is None or (today - self.last_scheduled).days >= 7
        return True

    def mark_complete(self) -> None:
        """Mark this task as completed and record today as the last scheduled date."""
        self.completed = True
        self.last_scheduled = date.today()

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
        """Filter due tasks, sort by priority then shortest duration, and greedily fit them
        into the owner's daily time budget. Sets last_scheduled on each chosen task and
        returns the list of scheduled tasks."""
        today = date.today()
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        sorted_tasks = sorted(
            (t for t in self.owner.get_all_tasks(self.task_list) if t.is_due(today)),
            key=lambda t: (priority_order[t.priority], t.duration)
        )

        time_remaining = self.owner.get_available_time()
        self.scheduled_tasks = []

        for task in sorted_tasks:
            if task.duration <= time_remaining:
                self.scheduled_tasks.append(task)
                task.last_scheduled = today
                time_remaining -= task.duration

        return self.scheduled_tasks

    def validate(self) -> List[str]:
        """Check task_list for problems before scheduling. Detects duplicate tasks (same name
        and pet) and total duration exceeding the owner's daily budget. Returns a list of
        warning strings — an empty list means no conflicts."""
        warnings = []

        seen = []
        for task in self.task_list:
            if task in seen:
                warnings.append(
                    f"Duplicate task: '{task.name}' for {task.pet.name} appears more than once"
                )
            else:
                seen.append(task)

        total = sum(t.duration for t in self.task_list)
        budget = self.owner.get_available_time()
        if total > budget:
            warnings.append(
                f"Total task time ({total} min) exceeds daily budget ({budget} min) by {total - budget} min"
            )

        return warnings

    def filter_tasks(self, pet_name: str | None = None, incomplete_only: bool = False) -> List[Task]:
        """Return a filtered subset of task_list without modifying it. Pass pet_name to keep
        only tasks for that pet, incomplete_only=True to exclude completed tasks. Both filters
        can be combined."""
        result = self.task_list
        if pet_name is not None:
            result = [t for t in result if t.pet.name == pet_name]
        if incomplete_only:
            result = [t for t in result if not t.completed]
        return result

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
