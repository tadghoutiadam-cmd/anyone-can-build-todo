# Plan: Add Due Dates to Tasks (Track C)

## 1. What it does
Allows users to optionally set a due date when creating a to-do item.
If a task has a due date, the date is displayed alongside the task title in the list (e.g. "Buy milk (Due: 2026-10-25)").
If no due date is provided, the task behaves exactly as before.

## 2. Decisions for the project owner
1. **Field constraints**: The due date should be optional (`null=True, blank=True`).
2. **HTML input type**: Use `<input type="date" name="due_date">` so standard browsers provide an accessible native date picker.
3. **Database migration**: Adding a field requires running `python manage.py makemigrations`.
4. **Display format**: When present, display in a small badge/span: `<span class="due-date">Due: YYYY-MM-DD</span>`.

## 3. Done when (Owner criteria)
- Submitting the add form with title "File taxes" and due date "2026-10-30" creates a task with `due_date == date(2026, 10, 30)`.
- The to-do item on the page displays its due date.
- Submitting an item without a due date leaves `due_date` as `None` without errors.
- Target test count: Increases from **6 to 8 tests** (adds 2 tests in `todos/tests.py`).

## 4. Files and functions touched
- `todos/models.py`: Add `due_date = models.DateField(null=True, blank=True)` to `Todo`.
- `todos/migrations/0002_todo_due_date.py`: Created via `makemigrations`.
- `todos/views.py`: In `todo_add`, read `due_date = request.POST.get("due_date") or None`.
- `todos/templates/todos/todo_list.html`: Add `<input type="date" name="due_date">` to add form, render `due_date` in the list item.
- `todos/tests.py`: Add `test_add_todo_with_due_date` and `test_todo_without_due_date_allowed`.

## 5. Objections and decisions (Maker-Checker Review)
| Objection / Edge Case | Assessment | Decision |
|---|---|---|
| What happens to existing database rows that don't have a due date? | `null=True, blank=True` allows existing rows to remain valid with `NULL` due dates. | **Accepted**: Database migration requires no default value and applies cleanly. |
| Should we reject due dates in the past? | Sometimes people record tasks that were due yesterday or earlier to log history. | **Rejected**: Do not enforce future-only validation; keep user input flexible. |
| Should we include time-of-day (DateTimeField)? | Most to-dos are day-based. Asking for exact hours/minutes adds form friction. | **Rejected**: Use `DateField` for simplicity and cleaner browser picker UI. |
