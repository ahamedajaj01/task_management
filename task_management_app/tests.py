from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task

class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.task = Task.objects.create(
            title="Initial Task",
            status="Pending",
            priority="Low"
        )

    def test_create_task_success(self):
        payload = {'title': 'New Task', 'status': 'InProgress', 'priority': 'High'}
        response = self.client.post('/api/create/task/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['task']['title'], 'New Task')

    def test_create_task_defaults(self):
        payload = {'title': 'Task Defaults'}
        response = self.client.post('/api/create/task/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['task']['status'], 'Pending')
        self.assertEqual(response.data['task']['priority'], 'Low')

    def test_create_task_validation_error(self):
        payload = {'status': 'Invalid'}
        response = self.client.post('/api/create/task/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_tasks_with_filtering_and_sorting(self):
        response = self.client.get('/api/list/tasks/?status=Pending&ordering=-id')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tasks', response.data)

    def test_get_single_task(self):
        response = self.client.get(f'/api/get/task/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.task.id)

    def test_update_task_put_and_patch(self):
        # PUT
        res_put = self.client.put(f'/api/update/task/{self.task.id}/', {'title': 'PUT Task'}, format='json')
        self.assertEqual(res_put.status_code, status.HTTP_200_OK)
        # PATCH
        res_patch = self.client.patch(f'/api/update/task/{self.task.id}/', {'status': 'Completed'}, format='json')
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.assertEqual(res_patch.data['task']['status'], 'Completed')

    def test_delete_task(self):
        response = self.client.delete(f'/api/delete/task/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
