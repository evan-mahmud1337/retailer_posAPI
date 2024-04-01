from rest_framework.permissions import BasePermission


class IsCustomAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.user_type in ['admin']
    
class IsManagerOrAbove(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.user_type in ['manager', 'admin']

class IsSerller(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.user_type in ['seller','manager', 'admin']
