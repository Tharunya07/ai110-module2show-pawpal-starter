import streamlit as st
from pawpal_system import Pet, Owner, Task, Scheduler, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session state init ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.title("🐾 PawPal+")
st.caption("A daily pet care scheduler for busy owners.")
st.divider()

# ─────────────────────────────────────────────
# SECTION 1 — Owner + Pet Setup
# ─────────────────────────────────────────────
st.subheader("1. Owner & Pet Setup")

with st.form("owner_form"):
    st.markdown("**Owner details**")
    owner_name = st.text_input("Owner name", value="Jamie")
    available_time = st.number_input("Available time per day (minutes)", min_value=10, max_value=480, value=90)

    st.markdown("**Pet details**")
    pet_name = st.text_input("Pet name", value="Biscuit")
    species = st.selectbox("Species", ["Dog", "Cat", "Rabbit", "Bird", "Other"])
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
    notes = st.text_area("Notes (health, behaviour, etc.)", value="Energetic, needs daily walks")

    submitted = st.form_submit_button("Save Owner & Pet")

if submitted:
    pet = Pet(name=pet_name, species=species, age=age, notes=notes)
    owner = Owner(name=owner_name, available_time_per_day=available_time, preferences=[], pets=[pet])
    scheduler = Scheduler(task_list=[], owner=owner)
    st.session_state.owner = owner
    st.session_state.scheduler = scheduler
    st.session_state.tasks = []
    st.success(f"Saved! Owner **{owner_name}** with pet **{pet_name}** ({species}).")

if st.session_state.owner:
    owner = st.session_state.owner
    st.info(
        f"Current owner: **{owner.name}** — "
        f"{owner.get_available_time()} min/day — "
        f"Pets: {', '.join(p.name for p in owner.pets)}"
    )

st.divider()

# ─────────────────────────────────────────────
# SECTION 2 — Add a Task
# ─────────────────────────────────────────────
st.subheader("2. Add a Task")

if st.session_state.owner is None:
    st.warning("Complete Section 1 first to set up an owner and pet.")
else:
    owner = st.session_state.owner
    scheduler = st.session_state.scheduler
    pet_map = {pet.name: pet for pet in owner.pets}

    with st.form("task_form"):
        pet_choice = st.selectbox("Pet", list(pet_map.keys()))
        task_name = st.text_input("Task name", value="Morning Walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
        priority_choice = st.selectbox("Priority", ["HIGH", "MEDIUM", "LOW"])
        category = st.text_input("Category", value="Exercise")

        task_submitted = st.form_submit_button("Add Task")

    if task_submitted:
        selected_pet = pet_map[pet_choice]
        priority = Priority[priority_choice]
        task = Task(
            name=task_name,
            duration=int(duration),
            priority=priority,
            category=category,
            pet=selected_pet,
        )
        scheduler.add_task(task)
        selected_pet.tasks.append(task)
        st.session_state.scheduler = scheduler
        st.session_state.tasks = scheduler.task_list
        st.success(f"Added: **{task_name}** for {selected_pet.name} ({priority_choice}, {int(duration)} min)")

    if st.session_state.tasks:
        st.markdown("**Current task list:**")
        for t in st.session_state.tasks:
            st.markdown(
                f"- **{t.name}** — {t.pet.name} | {t.priority.value.upper()} | {t.duration} min | _{t.category}_"
            )
    else:
        st.info("No tasks added yet.")

st.divider()

# ─────────────────────────────────────────────
# SECTION 3 — Generate Plan
# ─────────────────────────────────────────────
st.subheader("3. Generate Today's Plan")

if st.session_state.owner is None:
    st.warning("Complete Section 1 first to set up an owner and pet.")
elif not st.session_state.tasks:
    st.warning("Add at least one task in Section 2 before generating a plan.")
else:
    if st.button("Generate Today's Plan"):
        scheduler = st.session_state.scheduler
        plan = scheduler.generate_plan()

        if not plan:
            st.error("No tasks fit within the available time budget.")
        else:
            st.markdown("### Scheduled Tasks")
            for i, task in enumerate(plan, start=1):
                st.markdown(
                    f"**{i}. {task.name}**  \n"
                    f"Pet: {task.pet.name} &nbsp;|&nbsp; "
                    f"Priority: {task.priority.value.upper()} &nbsp;|&nbsp; "
                    f"Duration: {task.duration} min"
                )

            st.markdown("### Plan Reasoning")
            st.text(scheduler.explain_plan())
