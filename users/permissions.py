from rest_framework.permissions import BasePermission

class IsNotAuthenticated(BasePermission):

    message = "You're a registered user"

    def has_permission(self, request, view):
        return not request.user.is_authenticated