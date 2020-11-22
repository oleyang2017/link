from rest_framework import serializers

from .models import DeviceCategory, Device


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
