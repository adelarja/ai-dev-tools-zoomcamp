from django.test import TestCase
from django.urls import reverse
from .models import Todo


class TodoViewsTests(TestCase):
    def test_list_view_shows_todos(self):
        Todo.objects.create(title="Test todo")
        response = self.client.get(reverse("todo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test todo")

    def test_can_create_todo(self):
        response = self.client.post(
            reverse("todo_create"),
            {
                "title": "New Todo",
                "description": "Some description",
                "due_date": "2030-01-01",
                "is_completed": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 1)

    def test_can_update_todo(self):
        todo = Todo.objects.create(title="Old title")
        response = self.client.post(
            reverse("todo_update", args=[todo.pk]),
            {
                "title": "Updated title",
                "description": "",
                "due_date": "",
                "is_completed": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        todo.refresh_from_db()
        self.assertEqual(todo.title, "Updated title")

    def test_can_mark_todo_complete(self):
        todo = Todo.objects.create(title="Incomplete", is_completed=False)
        response = self.client.get(reverse("todo_complete", args=[todo.pk]))
        self.assertEqual(response.status_code, 302)
        todo.refresh_from_db()
        self.assertTrue(todo.is_completed)

    def test_can_delete_todo(self):
        todo = Todo.objects.create(title="To delete")
        response = self.client.post(reverse("todo_delete", args=[todo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)
