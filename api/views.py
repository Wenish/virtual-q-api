from rest_framework import viewsets
from .models import Queue, Ticket
from .serializers import QueueSerializer, TicketSerializer

class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer