"""Файл для тестирования API
Тесты реализованы для пользователей, задач, токенов."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Task

User = get_user_model()


class UserModelTest(APITestCase):
    """
    Тестирование модели пользователя.
    """
    def test_create_user(self):
        """
        Тест создания пользователя.
        """
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_superuser)


class TaskModelTest(APITestCase):
    """
    Тестирование модели задач.
    """
    def setUp(self):
        """
        Создание пользователя и задачи для тестирования.
        """
        self.user = User.objects.create_user(
            username='taskowner',
            password='testpass123'
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            owner=self.user
        )

    def test_task_creation(self):
        """
        Тест создания задачи.
        """
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.status, 'new')
        self.assertEqual(self.task.owner, self.user)
        self.assertEqual(str(self.task), 'Test Task')


class AuthTests(APITestCase):
    """
    Тестирование аутентификации пользователя.
    """
    def test_jwt_auth(self):
        User.objects.create_user(username='testuser', password='testpass123')

        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username': 'testuser', 'password': 'testpass123'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)


class TaskAPITests(APITestCase):
    """
    Тестирование API задач.
    """
    def setUp(self):
        """
        Создание пользователя и задачи для тестирования.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(
            title='Initial Task',
            description='Initial Description',
            owner=self.user
        )

    def test_get_tasks(self):
        """
        Тест получения задач.
        """
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        """
        Тест создания задачи.
        """
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'new'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().owner, self.user)

    def test_task_filter_by_owner(self):
        """
        Тест фильтрации задач по владельцу.
        """
        new_user = User.objects.create_user(username='newuser', password='testpass123')
        Task.objects.create(title='Other Task', owner=new_user)

        response = self.client.get(reverse('task-list'))
        self.assertEqual(len(response.data), 1)

    def test_update_task(self):
        """
        Тест обновления задачи.
        """
        url = reverse('task-detail', args=[self.task.id])
        data = {'title': 'Updated Task'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_delete_task(self):
        """
        Тест удаления задачи.
        """
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)


class UserAPITests(APITestCase):
    """Тестирование API пользователя."""
    def setUp(self):
        """Создание пользователя для тестирования."""
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass'
        )
        self.client.force_authenticate(user=self.admin)

    def test_get_users(self):
        """Тест получения пользователей."""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_via_api(self):
        """Тест создания пользователя через API."""
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse('password' in response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())


class DocumentationTests(APITestCase):
    """Тестирование документации."""
    def test_swagger_docs(self):
        """Тест документации Swagger."""
        response = self.client.get('/swagger/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redoc_docs(self):
        """Тест документации Redoc."""
        response = self.client.get('/redoc/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
