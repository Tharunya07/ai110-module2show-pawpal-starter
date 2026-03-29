from pawpal_system import Pet, Owner, Task, Scheduler, Priority


# --- Pets ---
dog = Pet(
    name="Biscuit",
    species="Dog",
    age=3,
    notes="Energetic golden retriever, needs daily walks and regular brushing"
)

cat = Pet(
    name="Mochi",
    species="Cat",
    age=6,
    notes="Indoor cat on daily thyroid medication, shy but affectionate"
)

# --- Tasks ---
morning_walk = Task(
    name="Morning Walk",
    duration=30,
    priority=Priority.HIGH,
    category="Exercise",
    pet=dog
)

dog_feeding = Task(
    name="Feeding",
    duration=10,
    priority=Priority.HIGH,
    category="Nutrition",
    pet=dog
)

cat_medication = Task(
    name="Thyroid Medication",
    duration=5,
    priority=Priority.HIGH,
    category="Medical",
    pet=cat
)

cat_feeding = Task(
    name="Feeding",
    duration=10,
    priority=Priority.HIGH,
    category="Nutrition",
    pet=cat
)

dog_grooming = Task(
    name="Brushing & Grooming",
    duration=20,
    priority=Priority.MEDIUM,
    category="Grooming",
    pet=dog
)

cat_playtime = Task(
    name="Interactive Playtime",
    duration=15,
    priority=Priority.MEDIUM,
    category="Enrichment",
    pet=cat
)

dog_training = Task(
    name="Training Session",
    duration=20,
    priority=Priority.LOW,
    category="Training",
    pet=dog
)

cat_grooming = Task(
    name="Coat Brushing",
    duration=10,
    priority=Priority.LOW,
    category="Grooming",
    pet=cat
)

# --- Owner ---
owner = Owner(
    name="Jamie",
    available_time_per_day=90,
    preferences=["morning routine", "health first"],
    pets=[dog, cat]
)

# --- Scheduler ---
scheduler = Scheduler(task_list=[], owner=owner)

for task in [morning_walk, dog_feeding, cat_medication, cat_feeding,
             dog_grooming, cat_playtime, dog_training, cat_grooming]:
    scheduler.add_task(task)

# --- Generate Plan ---
plan = scheduler.generate_plan()

# --- Output ---
print("=" * 50)
print("           TODAY'S SCHEDULE — PawPal+")
print("=" * 50)
print(f"Owner : {owner.name}")
print(f"Budget: {owner.get_available_time()} min/day")
print(f"Pets  : {dog.name} ({dog.species}), {cat.name} ({cat.species})")
print("-" * 50)

for i, task in enumerate(plan, start=1):
    print(f"{i}. {task.name}")
    print(f"   Pet      : {task.pet.name}")
    print(f"   Priority : {task.priority.value.upper()}")
    print(f"   Duration : {task.duration} min")
    print()

print("=" * 50)
print("           PLAN REASONING")
print("=" * 50)
print(scheduler.explain_plan())
print("=" * 50)
