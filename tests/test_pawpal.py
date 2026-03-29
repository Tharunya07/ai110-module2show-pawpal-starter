from pawpal_system import Pet, Task, Priority


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
