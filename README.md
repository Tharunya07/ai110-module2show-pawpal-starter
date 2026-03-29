# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

The scheduler goes beyond a simple priority queue:

- **Priority + duration sorting** — tasks are sorted by priority first (HIGH before MEDIUM before LOW), then by shortest duration within the same priority tier, so the most important and most efficient tasks fill the budget first.
- **Recurring tasks** — each task can be marked `"daily"` (always included) or `"weekly"` (included only if 7 or more days have passed since it was last scheduled). Non-recurring tasks are always considered.
- **Task filtering** — `filter_tasks()` returns a subset of the task list by pet name, completion status, or both, without modifying the original list.
- **Conflict detection** — `validate()` checks for duplicate tasks (same name and pet) and flags if the total task time exceeds the owner's daily budget, before scheduling runs.
