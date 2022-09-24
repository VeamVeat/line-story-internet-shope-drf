from rest_framework.permissions import BasePermission


class IsBlockedPermissions(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_blocked:
            return True
        return False
