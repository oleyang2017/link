from rest_framework import serializers

from base.base_serializers import BaseModelSerializer
from user.models.user_profile import UserProfile
from common.models.invite_record import InviteRecord


class InviteRecordSerializer(BaseModelSerializer):
    user_info = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_user_info(obj):
        user_info = (
            UserProfile.objects.filter(id=obj.create_user_id)
            .values("username", "avatar", "avatar_url")
            .first()
        )
        return user_info

    class Meta:
        model = InviteRecord
        fields = "__all__"
