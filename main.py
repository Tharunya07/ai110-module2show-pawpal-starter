from datetime import date, timedelta
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

today = date.today()

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

# Deliberate duplicate — same name + same pet as dog_feeding
dog_feeding_duplicate = Task(
    name="Feeding",
    duration=10,
    priority=Priority.HIGH,
    category="Nutrition",
    pet=dog
)

cat_feeding = Task(
    name="Feeding",
    duration=10,
    priority=Priority.HIGH,
    category="Nutrition",
    pet=cat
)

cat_medication = Task(
    name="Thyroid Medication",
    duration=5,
    priority=Priority.HIGH,
    category="Medical",
    pet=cat,
    recurrence="daily"
)

# Weekly recurring — last done 8 days ago → DUE today
dog_grooming = Task(
    name="Brushing & Grooming",
    duration=20,
    priority=Priority.MEDIUM,
    category="Grooming",
    pet=dog,
    recurrence="weekly",
    last_scheduled=today - timedelta(days=8)
)

# Weekly recurring — last done 3 days ago → NOT due today
cat_grooming = Task(
    name="Coat Brushing",
    duration=10,
    priority=Priority.LOW,
    category="Grooming",
    pet=cat,
    recurrence="weekly",
    last_scheduled=today - timedelta(days=3)
)

cat_playtime = Task(
    name="Interactive Playtime",
    duration=15,
    priority=Priority.MEDIUM,
    category="Enrichment",
    pet=cat
)

# Extra tasks to push total well over the 90 min budget
dog_training = Task(
    name="Training Session",
    duration=20,
    priority=Priority.LOW,
    category="Training",
    pet=dog
)

dog_bath = Task(
    name="Bath Time",
    duration=25,
    priority=Priority.LOW,
    category="Grooming",
    pet=dog
)

# --- Owner ---
owner = Owner(
    name="Jamie",
    available_time_per_day=90,
    preferences=["morning routine", "health first"],
    pets=[dog, cat]
)

# --- Scheduler ---
# Use append directly to bypass add_task's dedup check so the duplicate lands in task_list
scheduler = Scheduler(task_list=[], owner=owner)

for task in [morning_walk, dog_feeding, dog_feeding_duplicate, cat_feeding,
             cat_medication, dog_grooming, cat_grooming, cat_playtime,
             dog_training, dog_bath]:
    scheduler.task_list.append(task)

# ─────────────────────────────────────────────
# VALIDATE — run before generate_plan()
# ─────────────────────────────────────────────
warnings = scheduler.validate()

print("=" * 55)
print("            CONFLICT WARNINGS")
print("=" * 55)
if warnings:
    for w in warnings:
        print(f"  [!] {w}")
else:
    print("  No conflicts detected.")
print()

# ─────────────────────────────────────────────
# Capture due status before generate_plan() mutates last_scheduled
# ─────────────────────────────────────────────
due_status = {task.name + task.pet.name: task.is_due(today) for task in scheduler.task_list}

# --- Generate Plan (runs normally despite warnings) ---
plan = scheduler.generate_plan()

# ─────────────────────────────────────────────
# TODAY'S SCHEDULE
# ─────────────────────────────────────────────
print("=" * 55)
print("            TODAY'S SCHEDULE -- PawPal+")
print("=" * 55)
print(f"Owner : {owner.name}   Budget: {owner.get_available_time()} min/day")
print(f"Pets  : {dog.name} ({dog.species}), {cat.name} ({cat.species})")
print(f"Date  : {today}")
print("-" * 55)

for i, task in enumerate(plan, start=1):
    recurrence_label = f"  [{task.recurrence}]" if task.recurrence else ""
    print(f"{i}. {task.name}{recurrence_label}")
    print(f"   Pet      : {task.pet.name}")
    print(f"   Priority : {task.priority.value.upper()}")
    print(f"   Duration : {task.duration} min")
    print()

# ─────────────────────────────────────────────
# PLAN REASONING
# ─────────────────────────────────────────────
print("=" * 55)
print("                PLAN REASONING")
print("=" * 55)
print(scheduler.explain_plan())
print("=" * 55)
