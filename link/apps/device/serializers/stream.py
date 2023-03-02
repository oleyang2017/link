from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from device.models.chart import Chart
from device.models.stream import Stream
from base.base_serializers import BaseModelSerializer
from device.serializers.chart import ChartSerializer


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
        if not obj.show_chart:
            return {}
        chart = Chart.objects.filter(device=obj.device, streams=obj).first()
        return ChartSerializer(chart).data if chart else {}

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
            "chart_info",
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
        try:
            with transaction.atomic():
                stream = super(StreamSerializer, self).create(validated_data)
                if validated_data.get("show_chart"):
                    chart_info = self.initial_data.get("chart_info", {})
                    chart_info["device"] = device.id
                    chart_info["streams"] = [stream.id]
                    chart_serializer = ChartSerializer(data=chart_info, context=self.context)
                    chart_serializer.is_valid(raise_exception=True)
                    chart_serializer.save(create_user=self.context["request"].user)
            return stream
        except Exception as e:
            raise e

    def update(self, instance, validated_data):
        if "device" in validated_data and instance.device.id != validated_data["device"].id:
            print(instance.device.id)
            print(validated_data["device"].id)
            raise serializers.ValidationError("不可更改绑定设备")
        if "data_type" in validated_data and instance.data_type != validated_data["data_type"]:
            raise serializers.ValidationError("不可更改数据类型")
        if validated_data.get("show_chart"):
            chart = Chart.objects.filter(device=instance.device, streams=instance).first()
            chart_info = self.initial_data.get("chart_info", {})
            chart_info["streams"] = [instance.id]
            chart_serializer = ChartSerializer(data=chart_info, context=self.context)
            if not chart:
                chart_info["device"] = instance.device.id
                chart_serializer.is_valid(raise_exception=True)
                chart_serializer.save(create_user=self.context["request"].user)
            else:
                chart_info["last_update_user"] = self.context["request"].user
                chart_serializer.is_valid(raise_exception=True)
                chart_serializer.update(chart, chart_info)
        return super(StreamSerializer, self).update(instance, validated_data)
