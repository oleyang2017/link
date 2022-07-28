from rest_framework import serializers

from base.base_serializers import BaseModelSerializer
from common.models.invite_record import InviteRecord


class InviteRecordSerializer(BaseModelSerializer):
    class Meta:
        model = InviteRecord
        fields = "__all__"
