from rest_framework import serializers

from emqx.models.user import EMQXUser
from base.base_serializers import BaseModelSerializer

from user.models import UserProfile


class UserDetailSerializer(BaseModelSerializer):
    emqx_user = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_emqx_user(obj):
        emqx_user = EMQXUser.objects.filter(user=obj).first()
        if emqx_user:
            return {
                "username": emqx_user.username,
                "password": emqx_user.password,
            }
        else:
            return {}

    class Meta:
        model = UserProfile
        fields = "__all__"
