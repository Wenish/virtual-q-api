from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class IsQueueOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.queue.user == request.user