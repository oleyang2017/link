from rest_framework import serializers
from django.contrib.auth.models import Group

from base.base_serializers import BaseModelSerializer
from user.models.group_extend import GroupExtend


class GroupSerializer(BaseModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class GroupExtendSerializer(BaseModelSerializer):
    group = GroupSerializer(many=False)

    class Meta:
        model = GroupExtend
        fields = "__all__"
