from django.db import models
from django.contrib.auth.models import User

class Queue(models.Model):
    # Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    # Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    number = models.IntegerField(unique=True)
    status_choices = [(1, 'new'), (2, 'in progress'), (3, 'done')]
    status = models.IntegerField(choices=status_choices)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.queue.name + '_' + str(self.number)