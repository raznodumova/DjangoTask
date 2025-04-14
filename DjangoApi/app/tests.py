from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Task


class UserTests(APITestCase):
    """Тесты для модели пользователя."""

    def setUp(self):
        """Создание пользователя."""
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')

    def test_create_user(self):
        """Тест создания пользователя."""
        url = reverse('user-create')
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'test@test.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(username='newuser').email, 'test@test.com')


class TaskTests(APITestCase):
    """Тесты для модели задач."""
    def setUp(self):
        """Создание пользователя и задачи."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        self.client.force_authenticate(user=self.user)

        self.task1 = Task.objects.create(
            title='Task 1',
            description='Description 1',
            status='new',
            owner=self.user
        )
        self.task2 = Task.objects.create(
            title='Task 2',
            description='Description 2',
            status='new',
            owner=self.user
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword'
        )
        self.task_other_user = Task.objects.create(
            title="Other User's Task",
            description="Description",
            status='new',
            owner=self.other_user
        )

    def test_create_task(self):
        """Тест создания задачи."""
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'new'
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(Task.objects.get(title='New Task').owner, self.user)

    def test_update_task(self):
        """Тест обновления задачи."""
        url = reverse('task-detail', args=[self.task1.id])
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': 'in_progress'
        }
        response = self.client.put(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task')

    def test_delete_task(self):
        """Тест удаления задачи."""
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.delete(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_status_flow(self):
        """Тест процесса выполнения задачи."""
        task = Task.objects.create(
            title='Status Test',
            description='Test Status Flow',
            status='new',
            owner=self.user
        )

        response = self.client.patch(reverse('task-detail', args=[task.id]), {'status': 'in_progress'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.status, 'in_progress')

        response = self.client.patch(reverse('task-detail', args=[task.id]), {'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.status, 'completed')

    def test_list_tasks(self):
        """Тест получения списка задач."""
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def get_another_user_tasks(self):
        """Тест получения списка задач другого пользователя."""
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

