from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.contrib.auth.models import Group

from device.models.device import Device
from base.base_serializers import BaseModelSerializer
from user.models.group_extend import GroupExtend
from device.serializers.device import DeviceSerializer
from invite.models.invite_link import InviteLink
from user.serializers.group_extend import GroupSerializer
from invite.serializers.invite_record import InviteRecordSerializer


class InviteLinkSerializer(BaseModelSerializer):
    invited_count = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_invited_count(obj):
        return obj.invite_records.count()

    class Meta:
        model = InviteLink
        fields = "__all__"


class InviteLinkDetailSerializer(BaseModelSerializer):
    create_user = serializers.SerializerMethodField(read_only=True)
    invited_count = serializers.SerializerMethodField(read_only=True)
    records = serializers.SerializerMethodField(read_only=True)
    object_info = serializers.SerializerMethodField(read_only=True)
    permissions = serializers.JSONField(required=True)

    @staticmethod
    def get_create_user(obj):
        user = obj.create_user
        return {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
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
                return [InviteRecordSerializer(instance=record, many=False).data]
        else:
            return InviteRecordSerializer(obj.invite_records, many=True).data
        return []

    def validate(self, attrs):
        # 验证权限
        allowed_permissions = ["view_device", "change_device", "sub", "control"]
        diff = set(attrs.get("permissions", [])).difference(set(allowed_permissions))
        if diff:
            raise ValidationError(f"权限不正确: {diff}")

        # 如果不是设置订阅权限，则必须有查看设备权限
        if (
            attrs.get("invite_type") == "device"
            and attrs.get("permissions", []) != ["sub"]
            and "view_device" not in attrs.get("permissions", [])
        ):
            raise serializers.ValidationError("设备权限必须有可查看的权限")
        return super(InviteLinkDetailSerializer, self).validate(attrs)

    def update(self, instance, validated_data):
        # 只允许修改enable信息
        if not instance.enable:
            raise ValidationError("已关闭的邀请链接不可以修改")
        data = {}
        for k in ["enable", "last_update_user"]:
            if k in validated_data:
                data[k] = validated_data.pop(k)
        if validated_data:
            raise ValidationError("邀请链接不可修改非enable之外的信息")
        return super(InviteLinkDetailSerializer, self).update(instance, data)

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
