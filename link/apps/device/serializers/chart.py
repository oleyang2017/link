from rest_framework import serializers

from device.models.chart import Chart
from base.base_serializers import BaseModelSerializer


class ChartSerializer(BaseModelSerializer):
    stream_list = serializers.SerializerMethodField(read_only=True)
    device_name = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_stream_list(obj):
        """
        获取绑定的数据流
        """
        streams = obj.streams.all()
        return [{"id": stream.id, "name": stream.name} for stream in streams]

    @staticmethod
    def get_device_name(obj):
        """
        获取设备名称
        """
        return obj.device.name if obj.device else ""

    class Meta:
        model = Chart
        fields = (
            "id",
            "name",
            "stream_list",
            "created_time",
            "update_time",
            "device",
            "device_name",
            "theme",
            "option",
            "title",
            "chart_id",
            "streams",
        )
        read_only_fields = ("id", "chart_id", "created_time", "update_time")
        extra_kwargs = {
            "device": {
                "write_only": True,
                "error_messages": {"does_not_exist": "设备不存在！"},
            },
            "streams": {
                "write_only": True,
                "required": True,
                "error_messages": {"does_not_exist": "数据流不存在！"},
            },
        }

    def create(self, validated_data):
        if "streams" not in validated_data:
            raise serializers.ValidationError("创建图表时必须选取一个数据流！")
        # 如果绑定了设备，那么数据流只能是当前设备的数据流
        if validated_data["device"]:
            device = validated_data["device"]
            if not self.context["request"].user.has_perm("change_device", device):
                raise serializers.ValidationError("没有修改该设备的权限!")
            for stream in validated_data["streams"]:
                if stream.device != device:
                    raise serializers.ValidationError(f"不可绑定非'{device.name}'下的数据流！")
                if stream.data_type == "char_data":
                    raise serializers.ValidationError("字符型的数据流不可以用于图表显示")
        return super(ChartSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if "device" in validated_data:
            if instance.device != validated_data["device"]:
                raise serializers.ValidationError("不可更改绑定设备！")
            if "streams" in validated_data:
                for stream in validated_data["streams"]:
                    if stream.device != instance.device:
                        raise serializers.ValidationError(f"不可绑定非'{instance.device.name}'下的数据流！")
                    if stream.data_type == "char_data":
                        raise serializers.ValidationError("字符型的数据流不可以用于图表显示")
        return super(ChartSerializer, self).update(instance, validated_data)


class ChartInfoSerializer(BaseModelSerializer):
    class Meta:
        model = Chart
        read_only_fields = (
            "id",
            "name",
            "created_time",
            "create_user",
            "last_update_user",
            "update_time",
            "theme",
            "option",
            "title",
            "chart_id",
        )
        exclude = (
            "device",
            "streams",
        )
