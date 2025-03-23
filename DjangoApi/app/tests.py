from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Task


class UserTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')

    def test_create_user(self):
        url = reverse('user-create')
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'test@test.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(username='newuser').email, 'test@test.com')


class TaskTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.task1 = Task.objects.create(title='Task 1',
                                         description='Description 1', owner=self.user)
        self.task2 = Task.objects.create(title='Task 2', description='Description 2', owner=self.user)
        self.task_other_user = Task.objects.create(title="Other User's Task",
                                                   description="Description",
                                                   owner=User.objects.create_user(username="otheruser",
                                                                                  password="otherpassword"))

    def test_create_task(self):
        url = reverse('task-list')
        data = {'title': 'New Task', 'description': 'New Description', 'status': 'new'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(Task.objects.get(title='New Task').owner, self.user)

    def test_get_task_list(self):
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_task_detail(self):
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task 1')

    def test_update_task(self):
        url = reverse('task-detail', args=[self.task1.id])
        data = {'title': 'Updated Task', 'description': 'Updated Description', 'status': 'in_progress'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task1.id).title, 'Updated Task')

    def test_delete_task(self):
        url = reverse('task-detail', args=[self.task1.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_access_other_user(self):
        url = reverse('task-detail', args=[self.task_other_user.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
