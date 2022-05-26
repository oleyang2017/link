from django.conf import settings
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

    # def create(self, validated_data):
    #     if not validated_data.get("sequence"):
    #         last_category = DeviceCategory.objects.filter(
    #             create_user=self.context.get("request").user
    #         ).last()
    #         if last_category:
    #             validated_data["sequence"] = last_category.sequence + 1
    #     return super(DeviceCategorySerializer, self).create(validated_data)

    class Meta:
        model = DeviceCategory
        fields = ("id", "name", "sequence", "device_count")


class DeviceSerializer(BaseModelSerializer):
    class Meta:
        model = Device
        fields = ("id", "category", "name", "status", "image", "sequence")
        read_only_fields = ("id", "category", "name", "status", "image", "sequence")


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
        if not validated_data.get("device"):
            raise serializers.ValidationError("请选择绑定的设备!")
        if settings.MAX_STREAM_NUM:
            device = Device.objects.filter(
                id=validated_data["device"].id,
                create_user=self.context["request"].user,
            ).first()
            if not device:
                raise serializers.ValidationError("设备不存在！")
            if device.streams.count() >= settings.MAX_STREAM_NUM:
                raise serializers.ValidationError("超过每个设备最多可绑定数量！")
        return Stream.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if (
                "device" in validated_data
                and instance.device.id != validated_data["device"].id
        ):
            raise serializers.ValidationError("不可更改绑定设备")
        if (
                "data_type" in validated_data
                and instance.data_type != validated_data["data_type"]
        ):
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
        return obj.device.name

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
                "required": False,
                "error_messages": {"does_not_exist": "数据流不存在！"},
            },
        }

    def create(self, validated_data):
        if "device" not in validated_data:
            raise serializers.ValidationError("创建图表时必须绑定设备！")
        if validated_data["device"].create_user != validated_data["create_user"]:
            raise serializers.ValidationError("设备不存在！")
        if "streams" not in validated_data:
            raise serializers.ValidationError("创建图表时必须选取一个数据流！")
        for stream in validated_data["streams"]:
            if stream.device != validated_data["device"]:
                raise serializers.ValidationError(
                    "不可绑定非'{}'下的数据流！".format(validated_data["device"].name)
                )
            if stream.data_type == "char_data":
                raise serializers.ValidationError("字符型的数据流不可以用于图表显示")
        return super(ChartSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if "device" in validated_data and instance.device != validated_data["device"]:
            raise serializers.ValidationError("不可更改绑定设备！")
        if "streams" in validated_data:
            for stream in validated_data["streams"]:
                if stream.device != instance.device:
                    raise serializers.ValidationError(
                        "不可绑定非'{}'下的数据流！".format(instance.device.name)
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
            if self.initial_data.get(
                    "trigger_type"
            ) == "action" and not self.initial_data.get("action"):
                raise serializers.ValidationError("'动作'为必填项")
            if self.initial_data.get(
                    "trigger_type"
            ) == "action_item" and not self.initial_data.get("action_item"):
                raise serializers.ValidationError("'指令'为必填项")
            if self.initial_data.get(
                    "trigger_type"
            ) == "http" and not self.initial_data.get("url"):
                raise serializers.ValidationError("'url'为必填项")
            if (
                    self.initial_data.get("trigger_type") == "email"
                    and not self.context.get("request").user.email
            ):
                raise serializers.ValidationError("请先绑定邮箱")
        return super(TriggerSerializer, self).is_valid(raise_exception)

    def update(self, instance, validated_data):
        if "device" in validated_data:
            raise serializers.ValidationError("不可更改绑定设备")
        if "stream" in validated_data:
            raise serializers.ValidationError("不可更改绑定的数据流")
        # 删除原有的数据
        if (
                "trigger_type" in validated_data
                and validated_data["trigger_type"] != "email"
        ):
            setattr(instance, validated_data.get("trigger_type"), None)
        return super(TriggerSerializer, self).update(instance, validated_data)


class DeviceDetailSerializer(BaseModelSerializer):
    streams = StreamSerializer(many=True, required=False, read_only=True)
    charts = ChartSerializer(many=True, required=False, read_only=True)
    triggers = TriggerSerializer(many=True, required=False, read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)

    # image_list = serializers.SerializerMethodField(read_only=True)
    #
    # def get_image_list(self, instance):
    #     request = self.context.get('request')
    #     if instance.image:
    #         image_url = instance.image.url
    #         return request.build_absolute_uri(image_url)
    #     else:
    #         return ""

    @staticmethod
    def get_category_name(obj):
        """
        获取设备分类名称
        """
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

        return super(DeviceDetailSerializer, self).create(validated_data)
