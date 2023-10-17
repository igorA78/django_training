from rest_framework.permissions import BasePermission


class EducationItemAccess(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_authenticated
        elif request.method in ['POST', 'DELETE']:
            return request.user.is_authenticated and not self.user_is_moderator(request)
        elif request.method in ['PUT', 'PATCH']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.method in ['GET', 'PUT', 'PATCH']:
            return obj.owner == request.user or self.user_is_moderator(request)
        elif request.method == 'DELETE':
            return obj.owner == request.user
        else:
            return False

    @staticmethod
    def user_is_moderator(request):
        return request.user.groups.filter(name='moderator_group').exists()
