from rest_framework import serializers
from django.contrib.auth.models import Group

from base.base_serializers import BaseModelSerializer
from user.models.group_extend import GroupExtend
from user.models.user_profile import UserProfile


class GroupSerializer(BaseModelSerializer):
    members = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_members(obj):
        members = []
        for user in obj.user_set.values("username", "nickname", "avatar", "avatar_url").all():
            members.append(user)
        return members

    class Meta:
        model = Group
        fields = "__all__"


class GroupExtendSerializer(BaseModelSerializer):
    group = GroupSerializer(many=False)

    class Meta:
        model = GroupExtend
        fields = "__all__"
