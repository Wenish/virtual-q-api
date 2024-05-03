from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from api.models import Queue, Ticket

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

    def test_queue_name_blank(self):
        # Attempt to create a Queue with a blank name
        with self.assertRaises(IntegrityError):
            Queue.objects.create(user=self.user, name='')

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
