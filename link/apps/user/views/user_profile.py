from rest_framework.viewsets import ReadOnlyModelViewSet

from user.models.user_profile import UserProfile as User
from user.serializers.user_profile import UserDetailSerializer


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserDetailSerializer
    queryset = User.objects

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id).all()
