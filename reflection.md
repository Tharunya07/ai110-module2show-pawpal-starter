# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
- Briefly describe your initial UML design.
- A: I started with three core classes: Pet (stores name, species, age), Task (stores what needs to be done, how long it takes, and how urgent it is), and Scheduler (takes the task list and time budget and figures out what fits in the day). The idea was to keep data separate from logic that the Pet and Task just hold info, Scheduler does the thinking.
The three core actions a user can perform:
1. Add a pet: enter name, type, and basic info.
2. Add care tasks: add tasks like "morning walk" with duration and priority.
3. Generate a daily plan: app schedules tasks based on time available and priority.
I mapped this in a mermaid diagram.

- What classes did you include, and what responsibilities did you assign to each?
- A:  Pet stores the animal's basic info (name, species, age, notes). Task stores what needs to be done, how long it takes, its priority, and whether it is done. Owner stores the person's name, available time per day, and preferences. Scheduler is responsible for taking the task list, fitting tasks within the time budget, sorting by priority, and explaining why each task was included or skipped.

**b. Design changes**

- Did your design change during implementation?
A: Yes, after running the skeleton through Claude for a review, several structural issues came up that needed fixing before writing any real logic. Claude helped me understand the missing relationships and logic bottlenecks.

- If yes, describe at least one change and why you made it.
A: Yes. After AI review, I made two changes. First, changed Owner.pet to pets: List[Pet] so the app can support more than one pet. Second, replaced priority: str in Task with an enum (HIGH, MEDIUM, LOW) so sorting in generate_plan is reliable and not based on raw string comparison.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
