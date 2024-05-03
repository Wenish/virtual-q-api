from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from django.db.utils import IntegrityError
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
        # Attempt to create a Queue with a null user
        with self.assertRaises(IntegrityError):
            Queue.objects.create(name='Test Queue')

class TicketModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.queue = Queue.objects.create(user=self.user, name='Test Queue')
        self.ticket = Ticket.objects.create(user=self.user, queue=self.queue, number=1, status=1)

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.user, self.user)
        self.assertEqual(self.ticket.queue, self.queue)
        self.assertEqual(self.ticket.number, 1)
        self.assertEqual(self.ticket.status, 1)

    def test_ticket_number_unique_within_queue(self):
        # Attempt to create a ticket with the same number within the same queue
        with self.assertRaises(Exception):
            Ticket.objects.create(user=self.user, queue=self.queue, number=1, status=2)

class TicketModelNegativeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.queue = Queue.objects.create(user=self.user, name='Test Queue')

    def test_ticket_number_blank(self):
        # Attempt to create a Ticket with a blank number
        with self.assertRaises(IntegrityError):
            Ticket.objects.create(user=self.user, queue=self.queue, number=None, status=1)

    def test_ticket_status_invalid(self):
        # Attempt to create a Ticket with an invalid status
        with self.assertRaises(ValueError):
            Ticket.objects.create(user=self.user, queue=self.queue, number=1, status=5)

    def test_ticket_queue_null(self):
        # Attempt to create a Ticket with a null queue
        with self.assertRaises(IntegrityError):
            Ticket.objects.create(user=self.user, number=1, status=1)

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
        data = {'queue': self.queue.id, 'number': 1, 'status': 1, 'user': self.user.id}
        request = self.factory.post('/api/tickets/', data, QUERY_STRING='format=json')
        force_authenticate(request, self.user)
        response = TicketViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)