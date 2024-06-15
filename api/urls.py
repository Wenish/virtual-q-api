from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QueueViewSet, TicketViewSet, StatsView

router = DefaultRouter()
router.register(r'queues', QueueViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', StatsView.as_view(), name='stats'),
]