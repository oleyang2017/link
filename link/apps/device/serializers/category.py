from rest_framework import serializers

from base.base_serializers import BaseModelSerializer
from device.models.category import DeviceCategory


class DeviceCategorySerializer(BaseModelSerializer):
    device_count = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_device_count(obj):
        """
        获取该分类下面设备数量
        """
        return obj.devices.count()

    class Meta:
        model = DeviceCategory
        fields = ("id", "name", "sequence", "device_count")
