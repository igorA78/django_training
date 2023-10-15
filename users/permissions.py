from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return True
        elif view.action in ['update', 'partial_update', 'destroy']:
            return obj == request.user
        else:
            return False

    @staticmethod
    def user_is_moderator(request):
        return request.user.groups.filter(name='moderator_group').exists()
#
