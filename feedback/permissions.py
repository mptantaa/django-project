from rest_framework import permissions

class CanModerateFeedbacks(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy', 'filter_by_date']:
            if request.user.is_staff:
                return True
        elif view.action == 'create':
            return True
        return False
