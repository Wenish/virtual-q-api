from rest_framework import viewsets, permissions, exceptions, views, response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Queue, Ticket
from .serializers import QueueSerializer, TicketSerializer
from .permissions import IsOwner, IsQueueOwner, IsOwnerOrReadOnly
from .serializers import StatsSerializer

class QueueViewSet(viewsets.ModelViewSet):
    # pylint: disable-next=no-member
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__id']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    

class TicketViewSet(viewsets.ModelViewSet):
    # pylint: disable-next=no-member
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'status': ["in", "exact"],
        'queue_id': ["exact"],
        'user__id': ["exact"]
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner|IsQueueOwner]

    def perform_update(self, serializer):
        ticket_instance = serializer.instance
        if ticket_instance.queue.user != self.request.user:
            raise exceptions.PermissionDenied("You don't have permission to edit this ticket.")
        serializer.save()

class StatsView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, _request, _format=None):
            # pylint: disable-next=no-member
        total_queues = Queue.objects.count()
            # pylint: disable-next=no-member
        total_tickets = Ticket.objects.count()

        # pylint: disable-next=no-member
        tickets_by_status = Ticket.objects.values('status').annotate(count=Count('status'))
        tickets_by_status_dict = {status['status']: status['count'] for status in tickets_by_status}

        stats = {
            'total_queues': total_queues,
            'total_tickets': total_tickets,
            'tickets_by_status': tickets_by_status_dict,
        }

        serializer = StatsSerializer(stats)
        return response.Response(serializer.data)