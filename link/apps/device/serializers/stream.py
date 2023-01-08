from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from device.models.stream import Stream
from device.models.chart import Chart
from base.base_serializers import BaseModelSerializer
from device.serializers.chart import ChartInfoSerializer


class StreamSerializer(BaseModelSerializer):
    device_name = serializers.SerializerMethodField(read_only=True)
    data_type_name = serializers.SerializerMethodField(read_only=True)
    chart_info = serializers.SerializerMethodField(read_only=True)

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

    @staticmethod
    def get_chart_info(obj):
        chart = Chart.objects.filter(device=obj.device, streams=obj).first()
        return ChartInfoSerializer(chart).data if chart else {}

    class Meta:
        model = Stream
        fields = (
            "id",
            "stream_id",
            "device",
            "device_name",
            "name",
            "data_type",
            "data_type_name",
            "qos",
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
            "chart_info"
        )
        read_only_fields = ("id", "stream_id", "created_time", "update_time")
        validators = [
            UniqueTogetherValidator(
                queryset=Stream.objects.all(), fields=("device", "name"), message="同一设备数据流名称不能重复！"
            )
        ]

    def create(self, validated_data):
        device = validated_data.get("device")
        if settings.MAX_STREAM_NUM:
            if device.streams.count() >= settings.MAX_STREAM_NUM:
                raise serializers.ValidationError("超过每个设备最多可绑定数量！")
        return Stream.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if "device" in validated_data and instance.device.id != validated_data["device"].id:
            raise serializers.ValidationError("不可更改绑定设备")
        if "data_type" in validated_data and instance.data_type != validated_data["data_type"]:
            raise serializers.ValidationError("不可更改数据类型")
        return super(StreamSerializer, self).update(instance, validated_data)
