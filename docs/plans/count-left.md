# Plan: Count What's Left (Track A)

## 1. What it does
Above the to-do list, display the number of items that still need to be done.
For example, if there are 3 uncompleted items, display "3 to do".
If all items are done (or there are no items), display "0 to do" (or appropriate zero state).

## 2. Decisions for the project owner
1. **Wording**: Should it say "X to do", "X remaining", or "X items left"?
   - *Recommendation*: "X to do" (matching the slide specification).
2. **Pluralization**: Should 1 item say "1 to do" or "1 item left"?
   - *Recommendation*: Keep it simple with "X to do" (e.g. "1 to do", "2 to do").
3. **Completed tasks**: Should completed items be excluded from the count?
   - *Recommendation*: Yes, count only tasks where `done == False`.

## 3. Done when (Owner writes this)
<!-- The project owner writes this section to specify exact conditions and target test count -->
- When the page loads with 2 active tasks and 1 completed task, it should display "2 to do".
- When all tasks are completed or list is empty, it should display "0 to do".
- Target test count: increases from 5 to 6 tests (or 7 tests).

## 4. Files and functions touched
- `todos/views.py`: `todo_list` view function passes `remaining_count` (or calculates `Todo.objects.filter(done=False).count()`) into the template context.
- `todos/templates/todos/todo_list.html`: Render the counter above the list of tasks.
- `todos/tests.py`: Add `test_shows_count_of_remaining_todos` verifying the counter appears correctly.

## 5. Objections and decisions (Maker-Checker Review)
| Objection / Edge Case | Assessment | Decision |
|---|---|---|
| What if there are zero tasks in total? | Should display "0 to do" without crashing. | **Accepted**: QuerySet count handles an empty table safely and returns 0. |
| What if all tasks are marked done? | Counter should show "0 to do". | **Accepted**: Covered by `filter(done=False)`. |
| Performance if list grows large? | `Todo.objects.filter(done=False).count()` runs an efficient `SELECT COUNT(*)` in SQL. | **Accepted**: Standard Django pattern; does not load objects into memory. |
| Should we use client-side JavaScript to update the counter live without reloading? | Every action (Add, Done, Undo, Delete) already reloads the page via POST. Adding JS adds unnecessary complexity and breaks simple testing. | **Rejected**: Server-side Django rendering is simpler, completely reliable, and requires zero JavaScript dependencies. |
| Should we put the counter in an HTML `<footer>` element? | A `<footer>` placed directly in `<body>` is announced by screen readers as the landmark footer for the entire page. | **Rejected**: Use `<p class="counter">` above the list instead so assistive tools don't misinterpret page landmarks. |
