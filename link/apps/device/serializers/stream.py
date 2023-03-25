from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from drf_writable_nested.serializers import WritableNestedModelSerializer

from device.models.device import Device
from device.models.stream import Stream
from base.base_serializers import BaseModelSerializer
from device.serializers.chart import ChartDetailSerializer
from user.models.user_profile import UserProfile


def check_stream_count(device: Device):
    """
    检查设备下数据流数量是否超过最大限制
    """
    if settings.MAX_STREAM_NUM and device.streams.count() >= settings.MAX_STREAM_NUM:
        raise serializers.ValidationError("超过每个设备最多可创建数据流数量")


def check_device_permission(user: UserProfile, device: Device):
    """
    检查用户是否有修改设备的权限
    """
    if not user.has_perm("change_device", device):
        raise serializers.ValidationError("没有修改该设备的权限!")


class StreamListSerializer(BaseModelSerializer):
    class Meta:
        model = Stream
        fields = ("id", "name", "color")


class StreamDetailSerializer(BaseModelSerializer):
    chart = ChartDetailSerializer(required=False)
    device_name = serializers.SerializerMethodField(read_only=True)
    data_type_name = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_device_name(obj):
        """
        获取所属设备名称
        """
        return obj.device.name

    @staticmethod
    def get_data_type_name(obj):
        """
        获取数据类型名称
        """
        return obj.get_data_type_display()

    class Meta:
        model = Stream
        fields = (
            "id",
            "device",
            "chart",
            "device_name",
            "name",
            "data_type",
            "data_type_name",
            "unit",
            "unit_name",
            "created_time",
            "update_time",
            "show",
            "icon",
            "image",
            "color",
            "save_data",
            "show_chart",
        )
        read_only_fields = ("id", "created_time", "update_time")


class StreamCreateOrUpdateSerializer(WritableNestedModelSerializer):
    # 用于创建或更新数据流
    chart = ChartDetailSerializer(required=False)

    class Meta:
        model = Stream
        fields = (
            "id",
            "device",
            "chart",
            "name",
            "data_type",
            "unit",
            "unit_name",
            "show",
            "icon",
            "image",
            "color",
            "save_data",
            "show_chart",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Stream.objects.all(), fields=("device", "name"), message="同一设备数据流名称不能重复！"
            )
        ]

    def create(self, validated_data):
        device = validated_data.get("device")
        current_user = self.context["request"].user
        check_device_permission(current_user, device)
        check_stream_count(device)
        return super(StreamCreateOrUpdateSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("device", None)
        validated_data.pop("data_type", None)
        check_device_permission(self.context["request"].user, instance.device)
        return super(StreamCreateOrUpdateSerializer, self).update(instance, validated_data)


class StreamNestedCreateSerializer(WritableNestedModelSerializer):
    # 用于嵌套创建数据流
    chart = ChartDetailSerializer(required=False)

    class Meta:
        model = Stream
        fields = (
            "id",
            "chart",
            "name",
            "data_type",
            "unit",
            "unit_name",
            "show",
            "icon",
            "image",
            "color",
            "save_data",
            "show_chart",
        )

    def create(self, validated_data):
        validated_data["create_user"] = self.context["request"].user
        check_stream_count(validated_data.get("device"))
        return super(StreamNestedCreateSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        raise Exception("不可更新!")
