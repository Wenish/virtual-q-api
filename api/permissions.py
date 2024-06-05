from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class IsQueueOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.queue.user == request.user
    
class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user