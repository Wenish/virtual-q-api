from rest_framework import serializers
from .models import Queue, Ticket

class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'