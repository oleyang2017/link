from rest_framework import serializers

from .models import DeviceCategory, Device, Stream, Chart


class DeviceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceCategory
        fields = '__all__'
        extra_kwargs = {'create_user': {'write_only': True}}


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = '__all__'
        extra_kwargs = {'desc': {'write_only': True}, 'create_user': {'write_only': True}}


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

