from django.test import TestCase
from django.urls import reverse

from .models import Todo


class TodoTests(TestCase):
    def test_list_page_loads(self):
        response = self.client.get(reverse("todo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nothing to do yet")

    def test_add_a_todo(self):
        self.client.post(reverse("todo_add"), {"title": "Buy milk"})
        self.assertEqual(Todo.objects.get().title, "Buy milk")

    def test_empty_title_is_not_added(self):
        self.client.post(reverse("todo_add"), {"title": "   "})
        self.assertEqual(Todo.objects.count(), 0)

    def test_toggle_marks_done_and_back(self):
        todo = Todo.objects.create(title="Read chapter 3")
        self.client.post(reverse("todo_toggle", args=[todo.pk]))
        todo.refresh_from_db()
        self.assertTrue(todo.done)
        self.client.post(reverse("todo_toggle", args=[todo.pk]))
        todo.refresh_from_db()
        self.assertFalse(todo.done)

    def test_delete_removes_it(self):
        todo = Todo.objects.create(title="Call home")
        self.client.post(reverse("todo_delete", args=[todo.pk]))
        self.assertEqual(Todo.objects.count(), 0)

    def test_count_remaining_todos(self):
        Todo.objects.create(title="Task one", done=False)
        Todo.objects.create(title="Task two", done=False)
        Todo.objects.create(title="Task three", done=True)
        response = self.client.get(reverse("todo_list"))
        self.assertContains(response, "2 to do")
    def test_add_todo_with_due_date(self):
        self.client.post(
            reverse("todo_add"),
            {"title": "Submit assignment", "due_date": "2026-10-30"},
        )
        todo = Todo.objects.get(title="Submit assignment")
        self.assertEqual(str(todo.due_date), "2026-10-30")
        response = self.client.get(reverse("todo_list"))
        self.assertContains(response, "2026-10-30")

    def test_add_todo_without_due_date(self):
        self.client.post(reverse("todo_add"), {"title": "No due date task"})
        todo = Todo.objects.get(title="No due date task")
        self.assertIsNone(todo.due_date)

    def test_clear_finished_deletes_only_done_todos(self):
        Todo.objects.create(title="Active task", done=False)
        Todo.objects.create(title="Completed task 1", done=True)
        Todo.objects.create(title="Completed task 2", done=True)
        response = self.client.post(reverse("todo_clear_finished"))
        self.assertRedirects(response, reverse("todo_list"))
        self.assertEqual(Todo.objects.count(), 1)
        self.assertEqual(Todo.objects.first().title, "Active task")

    def test_clear_finished_button_visibility(self):
        Todo.objects.create(title="Active task", done=False)
        response = self.client.get(reverse("todo_list"))
        self.assertNotContains(response, "Clear finished")

        Todo.objects.create(title="Done task", done=True)
        response = self.client.get(reverse("todo_list"))
        self.assertContains(response, "Clear finished")
