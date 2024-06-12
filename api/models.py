from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

class Queue(models.Model):
    # Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.name)

class Ticket(models.Model):
    # Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE)
    number = models.IntegerField(editable=False)
    status_choices = [(1, 'new'), (2, 'in progress'), (3, 'done')]
    status = models.IntegerField(choices=status_choices)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        unique_together = ('queue', 'number')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'queue'],
                condition=Q(status__in=[1, 2]),
                name='unique_user_queue_for_new_or_in_progress'
            )
        ]

    def save(self, *args, **kwargs):
        if self.status not in [choice[0] for choice in self.status_choices]:
            raise ValueError('Invalid status value.')
        
        if not self.pk:
            # pylint: disable-next=no-member
            last_ticket = Ticket.objects.filter(queue=self.queue).order_by('-number').first()
            if last_ticket:
                self.number = last_ticket.number + 1
            else:
                self.number = 1
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.queue.name + '_' + str(self.number)