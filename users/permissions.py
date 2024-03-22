from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsNotAuthenticated(BasePermission):

    message = "You're a registered user"

    def has_permission(self, request, view):
        return not request.user.is_authenticated
    

class IsUnverified(BasePermission):

    message = "You're verified"

    def has_permission(self, request, view):
        return not request.user.is_verified
    

class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        if request.method not in SAFE_METHODS and bool(request.user.id == view.kwargs['pk']):
            return True

