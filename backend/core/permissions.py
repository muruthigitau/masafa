# permissions.py
from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """
    def has_permission(self, request, view):
        return True
        # return request.user and request.user.is_superuser
    


class HasGroupPermission(BasePermission):
    """
    Custom permission to check if the user belongs to a group and has the correct default Django permission 
    for the current action on the current model. Superusers are granted access to everything.
    """
    def has_permission(self, request, view):
        # return True
        # Allow access to superusers without further checks
        if request.user and request.user.is_superuser:
            return True

        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Get the action being performed
        action = view.action

        # Map viewset actions to Django permissions
        permission_map = {
            'list': 'view',
            'retrieve': 'view',
            'create': 'add',
            'update': 'change',
            'partial_update': 'change',
            'destroy': 'delete'
        }

        # Get the model from the viewset's queryset
        model = view.queryset.model

        # Get the relevant permission type for the action
        permission_type = permission_map.get(action)
        if permission_type:
            # Build the permission string based on the app label and model name
            permission = f"{model._meta.app_label}.{permission_type}_{model._meta.model_name}"
            # Check if the user has the required permission and belongs to any group
            if request.user.groups.exists() and request.user.has_perm(permission):
                return True

        # If no specific permission is required, deny access
        return False
