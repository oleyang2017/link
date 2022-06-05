from django.conf import settings
from django.db import transaction
from rest_framework import serializers

from base.base_serializers import BaseModelSerializer
from .models import DeviceCategory, Device, Stream, Chart, Trigger


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


class DeviceSerializer(BaseModelSerializer):
    class Meta:
        model = Device
        fields = ("id", "category", "name", "status", "image", "sequence", "create_user")
        read_only_fields = ("id", "category", "name", "status", "image", "sequence", "create_user")


class StreamSerializer(BaseModelSerializer):
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
            "stream_id",
            "device",
            "device_name",
            "name",
            "data_type",
            "data_type_name",
            "qos",
            "unit_name",
            "created_time",
            "update_time",
        )
        read_only_fields = ("id", "stream_id", "created_time", "update_time")

    def create(self, validated_data):
        device = validated_data.get("device")
        if not device:
            raise serializers.ValidationError("请选择绑定的设备!")
        if not self.context["request"].user.has_perm("change_device", device) and self.context.get("need_prem", True):
            raise serializers.ValidationError("没有修改该设备的权限!")
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
            "custom_settings",
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
                        raise serializers.ValidationError(
                            f"不可绑定非'{instance.device.name}'下的数据流！"
                        )
                    if stream.data_type == "char_data":
                        raise serializers.ValidationError("字符型的数据流不可以用于图表显示")
        return super(ChartSerializer, self).update(instance, validated_data)


class TriggerSerializer(BaseModelSerializer):
    class Meta:
        model = Trigger
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        if self.initial_data.get("trigger_type"):
            trigger_type = self.initial_data.get("trigger_type")
            if trigger_type == "action" and not self.initial_data.get("action"):
                raise serializers.ValidationError("'动作'为必填项")
            if trigger_type == "action_item" and not self.initial_data.get("action_item"):
                raise serializers.ValidationError("'指令'为必填项")
            if trigger_type == "http" and not self.initial_data.get("url"):
                raise serializers.ValidationError("'url'为必填项")
            if trigger_type == "email" and not self.context.get("request").user.email:
                raise serializers.ValidationError("请先绑定邮箱")
        return super(TriggerSerializer, self).is_valid(raise_exception)

    def update(self, instance, validated_data):
        if "device" in validated_data:
            raise serializers.ValidationError("不可更改绑定设备")
        if "stream" in validated_data:
            raise serializers.ValidationError("不可更改绑定的数据流")
        # 删除原有的数据
        if "trigger_type" in validated_data and validated_data["trigger_type"] != "email":
            setattr(instance, validated_data.get("trigger_type"), None)
        return super(TriggerSerializer, self).update(instance, validated_data)


class DeviceDetailSerializer(BaseModelSerializer):
    streams = StreamSerializer(many=True, required=False)
    charts = ChartSerializer(many=True, required=False)
    triggers = TriggerSerializer(many=True, required=False)
    category_name = serializers.SerializerMethodField(read_only=True)

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
