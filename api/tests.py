from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate, APITestCase
from api.models import Queue, Ticket
from api.views import QueueViewSet, TicketViewSet

class QueueModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.queue = Queue.objects.create(user=self.user, name='Test Queue')

    def test_queue_creation(self):
        self.assertEqual(self.queue.name, 'Test Queue')
        self.assertEqual(self.queue.user, self.user)

class QueueModelNegativeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_queue_user_null(self):
        with self.assertRaises(IntegrityError):
            Queue.objects.create(name='Test Queue')

class TicketModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.queue = Queue.objects.create(user=self.user, name='Test Queue')
        self.ticket = Ticket.objects.create(user=self.user, queue=self.queue, status=1)

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.user, self.user)
        self.assertEqual(self.ticket.queue, self.queue)
        self.assertEqual(self.ticket.number, 1)
        self.assertEqual(self.ticket.status, 1)

    def test_ticket_number_unique_within_queue(self):
        with self.assertRaises(Exception):
            Ticket.objects.create(user=self.user, queue=self.queue, status=2)

class TicketModelNegativeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.queue = Queue.objects.create(user=self.user, name='Test Queue')

    def test_ticket_status_invalid(self):
        with self.assertRaises(ValueError):
            Ticket.objects.create(user=self.user, queue=self.queue, status=5)

class QueueViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@test.com', password='test.1234')
        self.queue = Queue.objects.create(user=self.user, name='Test Queue 1')
        self.queue2 = Queue.objects.create(user=self.user, name='Test Queue 2')
        self.queue3 = Queue.objects.create(user=self.user, name='Test Queue 3')
        self.factory = RequestFactory()
        self.client = APIClient()

    def test_queue_list_view(self):
        request = self.factory.get('/api/queues/')
        request.user = self.user
        force_authenticate(request, self.user)
        response = QueueViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_queue_view(self):
        data = {'name': 'Test Queue', 'user': 1}
        request = self.factory.post('/api/queues/', data, QUERY_STRING='format=json')
        force_authenticate(request, self.user)
        response = QueueViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TicketViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@test.com', password='test.1234')
        self.queue = Queue.objects.create(user=self.user, name='Test Queue')
        self.factory = RequestFactory()
        self.client = APIClient()

    def test_ticket_list_view(self):
        request = self.factory.get('/api/tickets/')
        request.user = self.user
        force_authenticate(request, self.user)
        response = TicketViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ticket_view(self):
        data = {'queue': self.queue.id, 'status': 1, 'user': self.user.id}
        request = self.factory.post('/api/tickets/', data, QUERY_STRING='format=json')
        force_authenticate(request, self.user)
        response = TicketViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class StatsViewTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        
        self.queue1 = Queue.objects.create(user=self.user1, name='Queue 1')
        self.queue2 = Queue.objects.create(user=self.user2, name='Queue 2')

        Ticket.objects.create(user=self.user1, queue=self.queue1, status=1)
        Ticket.objects.create(user=self.user2, queue=self.queue1, status=2)
        Ticket.objects.create(user=self.user1, queue=self.queue2, status=3)
        Ticket.objects.create(user=self.user2, queue=self.queue2, status=1)
        Ticket.objects.create(user=self.user2, queue=self.queue2, status=3)
    def test_stats_view(self):
        url = reverse('stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_queues', response.data)
        self.assertIn('total_tickets', response.data)
        self.assertIn('tickets_by_status', response.data)
        
        self.assertEqual(response.data['total_queues'], 2)
        self.assertEqual(response.data['total_tickets'], 5)
        self.assertEqual(response.data['tickets_by_status']['1'], 2)
        self.assertEqual(response.data['tickets_by_status']['2'], 1)
        self.assertEqual(response.data['tickets_by_status']['3'], 2)