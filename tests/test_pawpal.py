from datetime import date, timedelta
from pawpal_system import Pet, Owner, Task, Scheduler, Priority


# ── helpers ───────────────────────────────────────────────────────────────────

def make_pet(name="Biscuit"):
    return Pet(name=name, species="Dog", age=3, notes="Test pet")

def make_owner(pet, minutes=90):
    return Owner(name="Jamie", available_time_per_day=minutes, preferences=[], pets=[pet])

def make_scheduler(owner):
    return Scheduler(task_list=[], owner=owner)


# ── original tests ─────────────────────────────────────────────────────────────

def test_task_completion():
    pet = Pet(name="Biscuit", species="Dog", age=3, notes="Loves morning walks")
    task = Task(name="Morning Walk", duration=30, priority=Priority.HIGH, category="Exercise", pet=pet)

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_task_addition_to_pet():
    pet = Pet(name="Mochi", species="Cat", age=6, notes="Needs daily medication")

    assert len(pet.tasks) == 0

    task = Task(name="Thyroid Medication", duration=5, priority=Priority.HIGH, category="Medical", pet=pet)
    pet.tasks.append(task)

    assert len(pet.tasks) == 1


# ── test plan: 7 new tests ─────────────────────────────────────────────────────

def test_scheduled_tasks_fit_within_budget():
    pet = make_pet()
    owner = make_owner(pet, minutes=90)
    scheduler = make_scheduler(owner)

    for name, duration in [("Walk", 40), ("Feed", 30), ("Groom", 30), ("Train", 25)]:
        scheduler.add_task(Task(name=name, duration=duration, priority=Priority.MEDIUM, category="Care", pet=pet))

    plan = scheduler.generate_plan()

    assert sum(t.duration for t in plan) <= 90


def test_priority_ordering_respected():
    pet = make_pet()
    owner = make_owner(pet)
    scheduler = make_scheduler(owner)

    scheduler.add_task(Task(name="Low Task",    duration=10, priority=Priority.LOW,    category="Care", pet=pet))
    scheduler.add_task(Task(name="Medium Task", duration=10, priority=Priority.MEDIUM, category="Care", pet=pet))
    scheduler.add_task(Task(name="High Task",   duration=10, priority=Priority.HIGH,   category="Care", pet=pet))

    plan = scheduler.generate_plan()
    priorities = [t.priority for t in plan]

    high_indices   = [i for i, p in enumerate(priorities) if p == Priority.HIGH]
    medium_indices = [i for i, p in enumerate(priorities) if p == Priority.MEDIUM]
    low_indices    = [i for i, p in enumerate(priorities) if p == Priority.LOW]

    assert max(high_indices) < min(medium_indices)
    assert max(medium_indices) < min(low_indices)


def test_same_priority_sorted_shortest_first():
    pet = make_pet()
    owner = make_owner(pet)
    scheduler = make_scheduler(owner)

    long_task  = Task(name="Long Task",  duration=30, priority=Priority.HIGH, category="Care", pet=pet)
    short_task = Task(name="Short Task", duration=5,  priority=Priority.HIGH, category="Care", pet=pet)

    scheduler.add_task(long_task)
    scheduler.add_task(short_task)

    plan = scheduler.generate_plan()

    assert plan.index(short_task) < plan.index(long_task)


def test_pet_with_no_tasks_returns_empty():
    pet = make_pet()
    owner = make_owner(pet)
    scheduler = make_scheduler(owner)

    plan = scheduler.generate_plan()

    assert plan == []


def test_all_tasks_exceed_budget_no_crash():
    pet = make_pet()
    owner = make_owner(pet, minutes=90)
    scheduler = make_scheduler(owner)

    for i in range(3):
        scheduler.add_task(Task(name=f"Big Task {i}", duration=60, priority=Priority.MEDIUM, category="Care", pet=pet))

    plan = scheduler.generate_plan()

    assert len(plan) < 3
    assert len(plan) >= 1


def test_weekly_task_not_due_is_excluded():
    pet = make_pet()
    owner = make_owner(pet)
    scheduler = make_scheduler(owner)

    not_due = Task(
        name="Weekly Groom",
        duration=20,
        priority=Priority.MEDIUM,
        category="Grooming",
        pet=pet,
        recurrence="weekly",
        last_scheduled=date.today() - timedelta(days=3),
    )
    scheduler.add_task(not_due)

    plan = scheduler.generate_plan()

    assert not_due not in plan


def test_validate_flags_duplicate_task():
    pet = make_pet()
    owner = make_owner(pet)
    scheduler = make_scheduler(owner)

    task_a = Task(name="Feeding", duration=10, priority=Priority.HIGH, category="Nutrition", pet=pet)
    task_b = Task(name="Feeding", duration=10, priority=Priority.HIGH, category="Nutrition", pet=pet)

    scheduler.task_list.append(task_a)
    scheduler.task_list.append(task_b)

    warnings = scheduler.validate()

    assert len(warnings) == 1
    assert "Feeding" in warnings[0]
