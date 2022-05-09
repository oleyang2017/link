from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    create_user = serializers.CreateOnlyDefault(default=serializers.CurrentUserDefault)

    def update(self, instance, validated_data):
        # create_user信息仅在create方法中使用
        if "create_user" in validated_data:
            validated_data.pop("create_user")
        return super(BaseModelSerializer, self).update(instance, validated_data)
