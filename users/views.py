from rest_framework import viewsets
from rest_framework.response import Response

from users.models import User
from users.permissions import UserPermission
from users.serializers import UserSerializer, UserPartialSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserPartialSerializer
    queryset = User.objects.all()
    permission_classes = [UserPermission]
    
    def retrieve(self, request, *args, **kwargs):
        if self.kwargs['pk'] == str(request.user.pk):
            instance = self.get_object()
            serializer = UserSerializer(instance)
            return Response(serializer.data)

        return super().retrieve(request, *args, **kwargs)