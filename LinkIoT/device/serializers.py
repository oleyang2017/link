from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable

from .models import DeviceCategory, Device, Stream, Chart


class DeviceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceCategory
        fields = '__all__'
        extra_kwargs = {'create_user': {'write_only': True}}


class DeviceSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    category = DeviceCategorySerializer(read_only=True)
    name = serializers.CharField(max_length=8)
    status = serializers.BooleanField(read_only=True)
    image = serializers.ImageField(allow_null=True)
    sequence = serializers.IntegerField(default=0)

    def create(self, validated_data):
        if settings.MAX_DEVICE_NUM:
            if self.context.get('user').devices.count() >= settings.MAX_DEVICE_NUM:
                raise NotAcceptable('超过最大创建数')
        validated_data['create_user'] = self.context.get('user')
        return Device.objects.create(**validated_data)


class StreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stream
        fields = '__all__'
        extra_kwargs = {'create_user': {'write_only': True}, 'device_id': {'write_only': True}}


class ChartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chart
        fields = '__all__'


class DeviceDetailSerializer(serializers.ModelSerializer):

    streams = StreamSerializer(many=True)
    charts = ChartSerializer(many=True)

    class Meta:
        model = Device
        fields = '__all__'

