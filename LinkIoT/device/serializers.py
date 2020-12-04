from django.conf import settings
from rest_framework import serializers

from .models import DeviceCategory, Device, Stream, Chart


class DeviceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceCategory
        fields = '__all__'
        extra_kwargs = {'create_user': {'write_only': True}}


class DeviceSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, required=False)
    category = serializers.CharField(source='category.id', write_only=True, required=False)
    name = serializers.CharField(max_length=8)
    status = serializers.BooleanField(read_only=True)
    image = serializers.ImageField(allow_null=True, required=False)
    sequence = serializers.IntegerField(default=0, required=False)

    def validate_category(self, category):
        if not self.context.get('user'):
            raise serializers.ValidationError('缺少用户！')
        category_obj = DeviceCategory.objects.filter(id=category, create_user=self.context.get('user'))
        if not category_obj:
            raise serializers.ValidationError('设备分类不存在！')
        else:
            return category_obj[0]

    def create(self, validated_data):
        if not self.context.get('user'):
            raise serializers.ValidationError('缺少用户！')
        if settings.MAX_DEVICE_NUM:
            if self.context.get('user').devices.count() >= settings.MAX_DEVICE_NUM:
                raise serializers.ValidationError('超过最大创建数！')
        validated_data['create_user'] = self.context.get('user')
        return Device.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
        instance.save()
        return instance


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

