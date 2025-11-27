# tasks/tests/test_tasks_api.py

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from tasks.models import Task


User = get_user_model()


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # create two users to test permissions
        self.user = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="password123",
        )
        self.other_user = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="password123",
        )

        # log in user1
        self.client.force_authenticate(user=self.user)

        # create some tasks
        self.task1 = Task.objects.create(
            title="Task 1",
            done=False,
            owner=self.user,
        )
        self.task2 = Task.objects.create(
            title="Task 2",
            done=True,
            owner=self.user,
        )
        self.other_task = Task.objects.create(
            title="Other user task",
            done=False,
            owner=self.other_user,
        )

        self.list_url = reverse("task-list")

    def test_list_tasks_returns_only_logged_in_users_tasks(self):
        """
        GET /api/tasks/ should return only tasks belonging to the authenticated user.
        """
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # only 2 tasks should be returned (task1 and task2)
        # API uses pagination, so response.data has 'results'
        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 2)
        returned_titles = {item["title"] for item in results}
        self.assertIn("Task 1", returned_titles)
        self.assertIn("Task 2", returned_titles)
        self.assertNotIn("Other user task", returned_titles)

    def test_create_task_with_valid_data(self):
        """
        POST /api/tasks/ should create a new task associated with the logged-in user.
        """
        payload = {
            "title": "New task",
            "done": False,
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(owner=self.user).count(), 3)
        self.assertEqual(response.data["title"], payload["title"])
        self.assertEqual(response.data["done"], payload["done"])

    def test_create_task_with_invalid_data(self):
        """
        POST /api/tasks/ with invalid data should return 400.
        Example: missing the 'title' field if it is required.
        """
        payload = {
            "done": False,
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_retrieve_task_of_logged_in_user(self):
        """
        GET /api/tasks/{id}/ should return the task of the authenticated user.
        """
        url = reverse("task-detail", args=[self.task1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.task1.id)
        self.assertEqual(response.data["title"], self.task1.title)

    def test_retrieve_task_of_other_user_should_give_404_or_403(self):
        """
        GET /api/tasks/{id}/ of another user should not be accessible.
        Depending on your logic, it may be 404 (more common) or 403.
        Adjust the assert according to your logic.
        """
        url = reverse("task-detail", args=[self.other_task.id])
        response = self.client.get(url)

        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_partial_update_task(self):
        """
        PATCH /api/tasks/{id}/ should allow partial update of a task.
        """
        url = reverse("task-detail", args=[self.task1.id])
        payload = {
            "done": True,
        }

        response = self.client.patch(url, payload, format="json")
        self.task1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.task1.done)

    def test_partial_update_task_of_other_user_not_allowed(self):
        """
        PATCH /api/tasks/{id}/ of another user should not be allowed.
        """
        url = reverse("task-detail", args=[self.other_task.id])
        payload = {"title": "Hacking task"}

        response = self.client.patch(url, payload, format="json")

        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_delete_task(self):
        """
        DELETE /api/tasks/{id}/ should delete the task of the logged-in user.
        """
        url = reverse("task-detail", args=[self.task1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_delete_task_of_other_user_not_allowed(self):
        """
        DELETE /api/tasks/{id}/ of another user should not be allowed.
        """
        url = reverse("task-detail", args=[self.other_task.id])
        response = self.client.delete(url)

        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
        # ensures the task still exists
        self.assertTrue(Task.objects.filter(id=self.other_task.id).exists())

    def test_list_tasks_requires_authentication(self):
        """
        Without authentication, the API should deny access to the task list.
        """
        client = APIClient()  # new client without auth
        response = client.get(self.list_url)

        # DRF with IsAuthenticated returns 403, not 401
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_task(self):
        """
        PUT /api/tasks/{id}/ should allow full update of a task.
        """
        url = reverse("task-detail", args=[self.task1.id])
        payload = {
            "title": "Completely updated task",
            "done": True,
        }

        response = self.client.put(url, payload, format="json")
        self.task1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task1.title, "Completely updated task")
        self.assertTrue(self.task1.done)

    def test_full_update_task_of_other_user_not_allowed(self):
        """
        PUT /api/tasks/{id}/ of another user should not be allowed.
        """
        url = reverse("task-detail", args=[self.other_task.id])
        payload = {
            "title": "Hacking task",
            "done": True,
        }

        response = self.client.put(url, payload, format="json")

        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_create_task_requires_authentication(self):
        """
        POST /api/tasks/ without authentication should deny access.
        """
        client = APIClient()  # new client without auth
        payload = {
            "title": "New task",
            "done": False,
        }
        response = client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_task_requires_authentication(self):
        """
        GET /api/tasks/{id}/ without authentication should deny access.
        """
        client = APIClient()  # new client without auth
        url = reverse("task-detail", args=[self.task1.id])
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task_requires_authentication(self):
        """
        PATCH /api/tasks/{id}/ without authentication should deny access.
        """
        client = APIClient()  # new client without auth
        url = reverse("task-detail", args=[self.task1.id])
        payload = {"done": True}
        response = client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task_requires_authentication(self):
        """
        DELETE /api/tasks/{id}/ without authentication should deny access.
        """
        client = APIClient()  # new client without auth
        url = reverse("task-detail", args=[self.task1.id])
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task_sets_owner_automatically(self):
        """
        POST /api/tasks/ should automatically set the owner to the authenticated user.
        """
        payload = {
            "title": "Auto-owned task",
            "done": False,
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(id=response.data["id"])
        self.assertEqual(task.owner, self.user)

    def test_create_task_ignores_owner_in_payload(self):
        """
        POST /api/tasks/ should ignore owner field if provided in payload.
        The task should belong to the authenticated user, not the one in payload.
        """
        payload = {
            "title": "Task with owner in payload",
            "done": False,
            "owner": self.other_user.id,  # trying to set different owner
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(id=response.data["id"])
        # owner should be the authenticated user, not other_user
        self.assertEqual(task.owner, self.user)
        self.assertNotEqual(task.owner, self.other_user)

    def test_update_task_cannot_change_owner(self):
        """
        PATCH /api/tasks/{id}/ should not allow changing the owner field.
        """
        url = reverse("task-detail", args=[self.task1.id])
        original_owner = self.task1.owner
        payload = {
            "owner": self.other_user.id,  # trying to change owner
        }

        response = self.client.patch(url, payload, format="json")
        self.task1.refresh_from_db()

        # owner should remain unchanged
        self.assertEqual(self.task1.owner, original_owner)
        self.assertNotEqual(self.task1.owner, self.other_user)

    def test_read_only_fields_in_response(self):
        """
        Response should include read-only fields: id, created_at, updated_at.
        """
        response = self.client.get(reverse("task-detail", args=[self.task1.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertIsNotNone(response.data["id"])
        self.assertIsNotNone(response.data["created_at"])
        self.assertIsNotNone(response.data["updated_at"])

    def test_list_tasks_ordered_by_created_at_desc(self):
        """
        GET /api/tasks/ should return tasks ordered by created_at descending (newest first).
        """
        # Create a new task (will be the newest)
        new_task = Task.objects.create(
            title="Newest task",
            done=False,
            owner=self.user,
        )

        response = self.client.get(self.list_url)
        results = response.data.get('results', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The newest task should be first
        self.assertEqual(results[0]["id"], new_task.id)

    def test_retrieve_non_existent_task(self):
        """
        GET /api/tasks/{invalid_id}/ should return 404.
        """
        url = reverse("task-detail", args=[99999])  # non-existent ID
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_non_existent_task(self):
        """
        PATCH /api/tasks/{invalid_id}/ should return 404.
        """
        url = reverse("task-detail", args=[99999])  # non-existent ID
        payload = {"done": True}
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existent_task(self):
        """
        DELETE /api/tasks/{invalid_id}/ should return 404.
        """
        url = reverse("task-detail", args=[99999])  # non-existent ID
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task_with_empty_title(self):
        """
        POST /api/tasks/ with empty title should return 400.
        """
        payload = {
            "title": "",
            "done": False,
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_task_with_title_too_long(self):
        """
        POST /api/tasks/ with title > 200 chars should return 400.
        """
        payload = {
            "title": "a" * 201,  # 201 characters (max is 200)
            "done": False,
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_update_task_with_invalid_data(self):
        """
        PATCH /api/tasks/{id}/ with invalid data should return 400.
        """
        url = reverse("task-detail", args=[self.task1.id])
        payload = {
            "title": "",  # empty title is invalid
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_create_task_with_done_default_false(self):
        """
        POST /api/tasks/ without 'done' field should default to False.
        """
        payload = {
            "title": "Task without done field",
        }

        response = self.client.post(self.list_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data["done"])

    def test_list_tasks_returns_empty_for_user_without_tasks(self):
        """
        GET /api/tasks/ should return empty list for user without tasks.
        """
        # Create a new user with no tasks
        new_user = User.objects.create_user(
            username="user3",
            email="user3@example.com",
            password="password123",
        )
        self.client.force_authenticate(user=new_user)

        response = self.client.get(self.list_url)
        results = response.data.get('results', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 0)
