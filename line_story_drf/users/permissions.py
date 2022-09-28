from rest_framework.permissions import BasePermission


class IsNotCurrentUserPermissions(BasePermission):

    def has_permission(self, request, view):
        if int(view.kwargs.get('id')) == request.user.pk:
            return False
        return True
