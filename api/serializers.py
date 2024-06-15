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
        
# pylint: disable-next=abstract-method'
class StatsSerializer(serializers.Serializer):
    total_queues = serializers.IntegerField()
    total_tickets = serializers.IntegerField()
    tickets_by_status = serializers.DictField(child=serializers.IntegerField())