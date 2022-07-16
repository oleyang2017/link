from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from base.base_serializers import BaseModelSerializer
from device.models.trigger import Trigger


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
