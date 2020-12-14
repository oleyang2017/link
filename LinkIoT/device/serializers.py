from django.conf import settings
from rest_framework import serializers

from .models import DeviceCategory, Device, Stream, Chart, Trigger, TriggerLog


class DeviceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceCategory
        fields = '__all__'
        extra_kwargs = {'create_user': {'write_only': True}}


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ('id', 'category', 'name', 'status', 'image', 'sequence')
        read_only_fields = ('id', 'category', 'name', 'status', 'image', 'sequence')


class StreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stream
        fields = '__all__'

    def create(self, validated_data):
        if settings.MAX_STREAM_NUM:
            device = Device.objects.filter(id=self.initial_data["device"], create_user=self.context.get('user'))
            if not device:
                raise serializers.ValidationError('设备不存在！')
            if device[0].streams.count() >= settings.MAX_STREAM_NUM:
                raise serializers.ValidationError('超过每个设备最多可绑定数量！')
        validated_data['create_user'] = self.context.get('user')
        return Stream.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'device' in validated_data:
            raise serializers.ValidationError('不可更改绑定设备')
        if 'data_type' in validated_data:
            raise serializers.ValidationError('不可更改数据类型')
        return super(StreamSerializer, self).update(instance, validated_data)


class ChartSerializer(serializers.ModelSerializer):
    stream_list = serializers.SerializerMethodField(read_only=True)

    def get_stream_list(self, obj):
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
                        'create_user': {'write_only': True},
                        'streams': {'write_only': True, 'required': False, 'error_messages': {'does_not_exist': '数据流不存在！'}}}
        
    def create(self, validated_data):
        if 'device' not in validated_data:
            raise serializers.ValidationError('创建图表时必须绑定设备！')
        if validated_data['device'].create_user != self.context.get('user'):
            raise serializers.ValidationError('设备不存在！')
        if 'streams' not in validated_data:
            raise serializers.ValidationError('创建图表时必须选取一个数据流！')
        for stream in validated_data.get('streams'):
            if stream.device != validated_data.get('device'):
                raise serializers.ValidationError("不可绑定非'{}'下的数据流！".format(validated_data.get('device').name))
            if stream.data_type == 'char_data':
                raise serializers.ValidationError("字符型的数据流不可以用于图表显示")
        return super(ChartSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'device' in validated_data:
            raise serializers.ValidationError('不可更改绑定设备！')
        if 'streams' in validated_data:
            for stream in validated_data['streams']:
                if stream.device != instance.device:
                    raise serializers.ValidationError("不可绑定非'{}'下的数据流！".format(instance.device.name))
                if stream.data_type == 'char_data':
                    raise serializers.ValidationError("字符型的数据流不可以用于图表显示")
        return super(ChartSerializer, self).update(instance, validated_data)


class DeviceDetailSerializer(serializers.ModelSerializer):
    streams = StreamSerializer(many=True, required=False)
    charts = ChartSerializer(many=True, required=False)

    class Meta:
        model = Device
        fields = ('id', 'client_id', 'category', 'name', 'desc', 'status', 'image', 'sequence', 'create_time',
                  'update_time', 'last_connect_time', 'streams', 'charts')
        read_only_fields = ('id', 'client_id', 'status', 'create_time', 'update_time', 'last_connect_time',)

    def is_valid(self, raise_exception=False):
        if self.initial_data.get("category"):
            category = DeviceCategory.objects.filter(id=self.initial_data["category"], create_user=self.context.get('user'))
            if not category:
                raise serializers.ValidationError('设备分类不存在！')
        return super(DeviceDetailSerializer, self).is_valid(raise_exception)

    def create(self, validated_data):
        if not self.context.get('user'):
            raise serializers.ValidationError('缺少用户！')
        if settings.MAX_DEVICE_NUM:
            if self.context.get('user').devices.count() >= settings.MAX_DEVICE_NUM:
                raise serializers.ValidationError('超过最大创建数！')
        validated_data['create_user'] = self.context.get('user')
        return Device.objects.create(**validated_data)


class TriggerSerializer(serializers.ModelSerializer):

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
            if self.initial_data.get('trigger_type') == 'email' and not self.context.get('user').email:
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

