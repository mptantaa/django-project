from rest_framework import permissions


class CanModeratePortfolios(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'partial_update', 'destroy', 'publish', 'patch']:
            return request.user.is_staff
        return True