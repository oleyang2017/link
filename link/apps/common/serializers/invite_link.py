from rest_framework import serializers
from django.contrib.auth.models import Group

from device.models.device import Device
from base.base_serializers import BaseModelSerializer
from user.models.group_extend import GroupExtend
from common.models.invite_link import InviteLink
from device.serializers.device import DeviceSerializer
from user.serializers.group_extend import GroupSerializer
from common.serializers.invite_record import InviteRecordSerializer


class InviteLinkSerializer(BaseModelSerializer):
    class Meta:
        model = InviteLink
        fields = "__all__"


class InviteLinkDetailSerializer(BaseModelSerializer):
    create_user = serializers.SerializerMethodField(read_only=True)
    invited_count = serializers.SerializerMethodField(read_only=True)
    records = serializers.SerializerMethodField(read_only=True)
    object_info = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_create_user(obj):
        user = obj.create_user
        return {
            "id": user.id,
            "username": user.username,
            "avatar_url": user.avatar_url,
        }

    @staticmethod
    def get_object_info(obj):
        if obj.invite_type == "device":
            device = Device.objects.filter(id=obj.object_id).first()
            return DeviceSerializer(instance=device).data
        else:
            group = Group.objects.filter(id=obj.object_id).first()
            return GroupSerializer(instance=group).data

    @staticmethod
    def get_invited_count(obj):
        return obj.invite_records.count()

    def get_records(self, obj):
        # 如果是所有者返回所有的记录，否则只返回自己的记录
        if self.context["request"].user != obj.create_user:
            record = obj.invite_records.filter(create_user=self.context["request"].user).first()
            if record:
                return InviteRecordSerializer(instance=record, many=True).data
        else:
            return InviteRecordSerializer(obj.invite_records, many=True).data
        return []

    def update(self, instance, validated_data):
        # 只允许修改enable信息
        if "enable" in validated_data:
            validated_data = {"enable": validated_data["enable"]}
        else:
            validated_data = {}
        return super(InviteLinkDetailSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        invite_type = validated_data["invite_type"]
        if invite_type == "device":
            device = Device.objects.filter(
                id=validated_data["object_id"],
                create_user=self.context["request"].user,
            ).first()
            if not device:
                raise serializers.ValidationError("设备不存在")
        else:
            group = GroupExtend.objects.filter(
                create_user=self.context["request"].user,
                group_id=validated_data["object_id"],
            ).first()
            if not group:
                raise serializers.ValidationError("群组不存在")
        return super(InviteLinkDetailSerializer, self).create(validated_data)

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
            "records",
            "object_info",
        )
