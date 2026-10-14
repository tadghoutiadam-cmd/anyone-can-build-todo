# Plan: Clear Finished To-Dos (Track B)

## 1. What it does
Adds a "Clear finished" button to the page. Clicking it deletes all completed to-do items (`done=True`) at once, leaving active items untouched.
If there are no finished to-dos, the button is either hidden or disabled so users cannot submit an unnecessary action.

## 2. Decisions for the project owner
1. **HTTP Method**: Must use `POST` (per rules in `AGENTS.md`: "Change data only with POST").
2. **URL Endpoint**: `/clear-finished/` mapped to view function `todo_clear_finished`.
3. **Visibility**: Show the button only when `Todo.objects.filter(done=True).exists()` is True (or pass `has_done_todos` in context).
4. **Behavior on empty list**: If no tasks are finished, doing a POST redirects safely back to the list with 0 deletions.

## 3. Done when (Owner criteria)
- When there are 2 completed tasks and 1 uncompleted task, clicking "Clear finished" deletes the 2 completed tasks and keeps the 1 uncompleted task.
- The button only appears when at least one task is marked `done=True`.
- When all tasks are active (none done), no "Clear finished" button is visible in the HTML.
- Target test count: Increases from **6 to 8 tests** (adds 2 tests in `todos/tests.py`).

## 4. Files and functions touched
- `todos/urls.py`: Add route `path("clear-finished/", views.todo_clear_finished, name="todo_clear_finished")`.
- `todos/views.py`:
  - Update `todo_list` context to include `has_done_todos = Todo.objects.filter(done=True).exists()`.
  - Add `@require_POST def todo_clear_finished(request)`.
- `todos/templates/todos/todo_list.html`: Render the "Clear finished" form/button below or near the list when `has_done_todos` is True.
- `todos/tests.py`: Add `test_clear_finished_deletes_only_done_todos` and `test_clear_finished_button_hidden_when_no_completed_todos`.

## 5. Objections and decisions (Maker-Checker Review)
| Objection / Edge Case | Assessment | Decision |
|---|---|---|
| What if someone posts to `/clear-finished/` when no items are done? | Calling `Todo.objects.filter(done=True).delete()` when empty safely does nothing. | **Accepted**: Django ORM handles deleting an empty queryset safely. |
| Should we show a confirmation dialog ("Are you sure?") using JavaScript? | Adding client-side JavaScript adds external complexity and requires browser-level tests. | **Rejected**: Keep the app purely server-driven; users can easily recreate tasks if needed. |
| Should "Clear finished" be a link using a `GET` request? | Violates the rule: "Change data only with POST. A GET request only reads." | **Rejected**: Must be a `<form method="post">` button to protect against CSRF and accidental crawler deletions. |
