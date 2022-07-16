from django.db import transaction
from django.conf import settings
from rest_framework import serializers

from device.models.device import Device
from base.base_serializers import BaseModelSerializer
from device.models.category import DeviceCategory
from device.serializers.chart import ChartSerializer
from device.serializers.stream import StreamSerializer
from device.serializers.trigger import TriggerSerializer


class DeviceSerializer(BaseModelSerializer):

    display_custom_info = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_display_custom_info(obj):
        return obj.get_display_custom_info()

    class Meta:
        model = Device
        fields = (
            "id",
            "category",
            "name",
            "status",
            "image",
            "sequence",
            "create_user",
            "display_custom_info",
        )
        read_only_fields = (
            "id",
            "category",
            "name",
            "status",
            "image",
            "sequence",
            "create_user",
            "display_custom_info",
        )


class DeviceDetailSerializer(BaseModelSerializer):
    streams = StreamSerializer(many=True, required=False, read_only=True)
    charts = ChartSerializer(many=True, required=False, read_only=True)
    triggers = TriggerSerializer(many=True, required=False, read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    display_custom_info = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_display_custom_info(obj):
        return obj.get_display_custom_info()

    @staticmethod
    def get_category_name(obj):
        if obj.category:
            return obj.category.name
        else:
            return None

    class Meta:
        model = Device
        fields = (
            "id",
            "client_name",
            "client_id",
            "category",
            "category_name",
            "name",
            "desc",
            "status",
            "image",
            "sequence",
            "created_time",
            "update_time",
            "last_connect_time",
            "streams",
            "charts",
            "triggers",
            "token",
            "custom_info",
            "display_custom_info",
        )
        read_only_fields = (
            "id",
            "client_name",
            "client_id",
            "status",
            "created_time",
            "update_time",
            "last_connect_time",
        )

    def is_valid(self, raise_exception=False):
        if self.initial_data.get("category"):
            category = DeviceCategory.objects.filter(
                id=self.initial_data["category"],
                create_user=self.context["request"].user,
            ).first()
            if not category:
                raise serializers.ValidationError("设备分类不存在！")
        return super(DeviceDetailSerializer, self).is_valid(raise_exception)

    def create(self, validated_data):
        if settings.MAX_DEVICE_NUM:
            current_num = Device.objects.filter(
                create_user=self.context["request"].user,
            ).count()
            if current_num >= settings.MAX_DEVICE_NUM:
                raise serializers.ValidationError("超过最大创建数！")
        try:
            with transaction.atomic():
                instance = super(DeviceDetailSerializer, self).create(validated_data)
                if validated_data.get("streams"):
                    stream_list = validated_data.pop("streams")
                    self.context["need_prem"] = False
                    for stream in stream_list:
                        stream["device"] = instance.id
                        stream_serializer = StreamSerializer(data=stream, context=self.context)
                        stream_serializer.is_valid(raise_exception=True)
                        stream_serializer.save(create_user=self.context["request"].user)
                return instance
        except Exception as e:
            raise e
