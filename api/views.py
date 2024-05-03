from rest_framework import viewsets, permissions, exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .models import Queue, Ticket
from .serializers import QueueSerializer, TicketSerializer
from .permissions import IsOwner, IsQueueOwner

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
    permission_classes = [permissions.IsAuthenticated, IsOwner|IsQueueOwner]

    def perform_update(self, serializer):
        ticket_instance = serializer.instance
        if ticket_instance.queue.user != self.request.user:
            raise exceptions.PermissionDenied("You don't have permission to edit this ticket.")
        serializer.save()