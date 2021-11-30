from django.conf import settings
from rest_framework import serializers

from .models import DeviceCategory, Device, Stream, Chart, Trigger, TriggerLog
from base.base_serializers import BaseModelSerializer


class DeviceCategorySerializer(BaseModelSerializer):
    device_count = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_device_count(obj):
        """
        获取该分类下面设备数量
        :param obj: DeviceCategory
        :return: int
        """
        return obj.devices.count()

    def create(self, validated_data):
        if not validated_data.get('sequence'):
            last_category = DeviceCategory.objects.filter(create_user=self.context.get('request').user).last()
            if last_category:
                validated_data['sequence'] = last_category.sequence + 1
        return super(DeviceCategorySerializer, self).create(validated_data)

    class Meta:
        model = DeviceCategory
        fields = '__all__'


class DeviceSerializer(BaseModelSerializer):

    class Meta:
        model = Device
        fields = ('id', 'category', 'name', 'status', 'image', 'sequence')
        read_only_fields = ('id', 'category', 'name', 'status', 'image', 'sequence')


class StreamSerializer(BaseModelSerializer):
    device_name = serializers.SerializerMethodField(read_only=True)
    data_type_name = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_device_name(obj):
        """
        获取所属设备名称
        :param obj: DeviceCategory
        :return: string
        """
        return obj.device.name

    @staticmethod
    def get_data_type_name(obj):
        """
        获取数据类型名称
        :param obj: DeviceCategory
        :return: string
        """
        return obj.get_data_type_display()

    class Meta:
        model = Stream
        fields = '__all__'

    def create(self, validated_data):
        if settings.MAX_STREAM_NUM:
            device = Device.objects.filter(id=self.initial_data["device"])
            if not device:
                raise serializers.ValidationError('设备不存在！')
            if device[0].streams.count() >= settings.MAX_STREAM_NUM:
                raise serializers.ValidationError('超过每个设备最多可绑定数量！')
        return Stream.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'device' in validated_data and instance.device != validated_data['device']:
            raise serializers.ValidationError('不可更改绑定设备')
        if 'data_type' in validated_data and instance.data_type != validated_data['data_type']:
            raise serializers.ValidationError('不可更改数据类型')
        return super(StreamSerializer, self).update(instance, validated_data)


class ChartSerializer(BaseModelSerializer):
    stream_list = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_stream_list(obj):
        """
        自定义数据流显示格式
        :param obj: chart object
        :return: List[dict]
        """
        streams = obj.streams.all()
        return [{'id': stream.id, 'name': stream.name} for stream in streams]

    class Meta:
        model = Chart
        exclude = ('create_time',)
        extra_kwargs = {'device': {'write_only': True, 'error_messages': {'does_not_exist': '设备不存在！'}},
                        'streams': {'write_only': True, 'required': False, 'error_messages': {'does_not_exist': '数据流不存在！'}}}
        
    def create(self, validated_data):
        if 'device' not in validated_data:
            raise serializers.ValidationError('创建图表时必须绑定设备！')
        if validated_data['device'].create_user != validated_data['user']:
            raise serializers.ValidationError('设备不存在！')
        if 'streams' not in validated_data:
            raise serializers.ValidationError('创建图表时必须选取一个数据流！')
        for stream in validated_data['streams']:
            if stream.device != validated_data['device']:
                raise serializers.ValidationError("不可绑定非'{}'下的数据流！".format(validated_data['device'].name))
            if stream.data_type == 'char_data':
                raise serializers.ValidationError("字符型的数据流不可以用于图表显示")
        return super(ChartSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'device' in validated_data and instance.device != validated_data['device']:
            raise serializers.ValidationError('不可更改绑定设备！')
        if 'streams' in validated_data:
            for stream in validated_data['streams']:
                if stream.device != instance.device:
                    raise serializers.ValidationError("不可绑定非'{}'下的数据流！".format(instance.device.name))
                if stream.data_type == 'char_data':
                    raise serializers.ValidationError("字符型的数据流不可以用于图表显示")
        return super(ChartSerializer, self).update(instance, validated_data)


class TriggerSerializer(BaseModelSerializer):

    class Meta:
        model = Trigger
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        if self.initial_data.get('trigger_type'):
            if self.initial_data.get('trigger_type') == 'action' and not self.initial_data.get('action'):
                raise serializers.ValidationError("'动作'为必填项")
            if self.initial_data.get('trigger_type') == 'action_item' and not self.initial_data.get('action_item'):
                raise serializers.ValidationError("'指令'为必填项")
            if self.initial_data.get('trigger_type') == 'http' and not self.initial_data.get('url'):
                raise serializers.ValidationError("'url'为必填项")
            if self.initial_data.get('trigger_type') == 'email' and not self.context.get('request').user.email:
                raise serializers.ValidationError("请先绑定邮箱")
        return super(TriggerSerializer, self).is_valid(raise_exception)

    def update(self, instance, validated_data):
        if 'device' in validated_data:
            raise serializers.ValidationError('不可更改绑定设备')
        if 'stream' in validated_data:
            raise serializers.ValidationError('不可更改绑定的数据流')
        # 删除原有的数据
        if 'trigger_type' in validated_data and validated_data['trigger_type'] != 'email':
            setattr(instance, validated_data.get('trigger_type'), None)
        return super(TriggerSerializer, self).update(instance, validated_data)


class DeviceDetailSerializer(BaseModelSerializer):
    streams = StreamSerializer(many=True, required=False)
    charts = ChartSerializer(many=True, required=False)
    triggers = TriggerSerializer(many=True, required=False)
    category_name = serializers.SerializerMethodField(read_only=True)
    # image_list = serializers.SerializerMethodField(read_only=True)

    # def get_image_list(self, instance):
    #     request = self.context.get('request')
    #     if instance.image:
    #         image_list = instance.image.url
    #         return [{'url': request.build_absolute_uri(image_list)}]
    #     else:
    #         return []

    @staticmethod
    def get_category_name(obj):
        """
        获取设备分类名称
        :param obj: device object
        :return: List[dict]
        """
        if obj.category:
            return obj.category.name
        else:
            return None

    class Meta:
        model = Device
        fields = ('id', 'client_id', 'category', 'category_name', 'name', 'desc', 'status', 'image', 'sequence', 'created_time',
                  'update_time', 'last_connect_time', 'streams', 'charts', 'create_user', 'triggers')
        read_only_fields = ('id', 'client_id', 'status', 'created_time', 'update_time', 'last_connect_time')

    def is_valid(self, raise_exception=False):
        if self.initial_data.get("category"):
            category = DeviceCategory.objects.filter(id=self.initial_data["category"], create_user=self.context.get('request').user)
            if not category:
                raise serializers.ValidationError('设备分类不存在！')
        return super(DeviceDetailSerializer, self).is_valid(raise_exception)

    def create(self, validated_data):
        if settings.MAX_DEVICE_NUM:
            if Device.objects.count() >= settings.MAX_DEVICE_NUM:
                raise serializers.ValidationError('超过最大创建数！')
        print(self.context['request'].user)
        print(validated_data)
        return Device.objects.create(**validated_data)


