from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the ticket
        return obj.user == request.user