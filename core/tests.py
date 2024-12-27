from django.test import TestCase
from django.urls import reverse
from mysql.connector.django import client
from rest_framework import status
from rest_framework.test import APIClient
from .models import Project, Task, Role, ProjectMember, UserRole, Notification, UserCommunicationChannel
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()

class TaskAPITest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('migrate')

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email="test@test.com",
            phone_number="123456"
        )
        self.role = Role.objects.create(name="testRole")
        self.project = Project.objects.create(name='Test Project', owner=self.user)

        self.task = Task.objects.create(name="Test Task", project=self.project, assignee=self.user)

        self.project_member = ProjectMember.objects.create(user=self.user, project=self.project)
        self.user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.notification = Notification.objects.create(user=self.user, message="test notification",
                                                        notification_type="test")
        self.user_communication_channel = UserCommunicationChannel.objects.create(
            user=self.user,
            platform="email",  # Corrected
            platform_id="test@test.com"  # Corrected
        )
        print(self.project.id)
        self.client.force_authenticate(user=self.user)


    def test_create_task(self):
        url = reverse('task-list-create')
        data = {'name': 'New Task', 'project': self.project.id, 'assignee': self.user.id, "description":"test", "due_date":"2024-12-12", "status":"In progress", "priority":"High"}
        print(data)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.latest('id').name, 'New Task')

    def test_get_task_list(self):
        url = reverse('task-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_task(self):
        url = reverse('task-retrieve-update-destroy', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task(self):
        url = reverse('task-retrieve-update-destroy', kwargs={'pk': self.task.id})
        data = {'name': 'Updated Task', 'project': self.project.id, 'assignee': self.user.id, "description":"test", "due_date":"2024-12-12", "status":"In progress", "priority":"High"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=self.task.id).name, 'Updated Task')

    def test_delete_task(self):
        url = reverse('task-retrieve-update-destroy', kwargs={'pk': self.task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

