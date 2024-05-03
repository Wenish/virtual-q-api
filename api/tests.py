from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Queue, Ticket

class QueueModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.queue = Queue.objects.create(user=self.user, name='Test Queue')

    def test_queue_creation(self):
        self.assertEqual(self.queue.name, 'Test Queue')
        self.assertEqual(self.queue.user, self.user)

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