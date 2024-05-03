from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .models import Queue, Ticket
from .serializers import QueueSerializer, TicketSerializer
from .permissions import IsOwner

class QueueViewSet(viewsets.ModelViewSet):
    # pylint: disable-next=no-member
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__id']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    

class TicketViewSet(viewsets.ModelViewSet):
    # pylint: disable-next=no-member
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'queue_id', 'user__id']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]