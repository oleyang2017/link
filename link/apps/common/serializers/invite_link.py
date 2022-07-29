from rest_framework import serializers

from base.base_serializers import BaseModelSerializer
from common.models.invite_link import InviteLink
from common.serializers.invite_record import InviteRecordSerializer


class InviteLinkSerializer(BaseModelSerializer):
    class Meta:
        model = InviteLink
        fields = "__all__"


class InviteLinkDetailSerializer(BaseModelSerializer):
    create_user = serializers.SerializerMethodField(read_only=True)
    invited_count = serializers.SerializerMethodField(read_only=True)
    record = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_create_user(obj):
        user = obj.create_user
        return {
            "id": user.id,
            "username": user.username,
            "avatar_url": user.avatar_url,
        }

    @staticmethod
    def get_invited_count(obj):
        return obj.invite_records.count()

    def get_record(self, obj):
        record = obj.invite_records.filter(create_user=self.context["request"].user).first()
        if record:
            return InviteRecordSerializer(instance=record).data
        else:
            return {}

    def update(self, instance, validated_data):
        # 只允许修改enable信息
        if "enable" in validated_data:
            validated_data = {"enable": validated_data["enable"]}
        else:
            validated_data = {}
        return super(InviteLinkDetailSerializer, self).update(instance, validated_data)

    class Meta:
        model = InviteLink
        fields = (
            "id",
            "created_time",
            "update_time",
            "code",
            "end_time",
            "count",
            "invite_type",
            "object_id",
            "permissions",
            "enable",
            "create_user",
            "invited_count",
            "record",
        )
