from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from base.base_serializers import BaseModelSerializer
from control.models.automation import Automation
from control.serializers.command import CommandSerializer


class AutomationListSerializer(BaseModelSerializer):

    display_automation_type = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_display_automation_type(obj):
        return obj.get_utomation_type_display()

    class Meta:
        model = Automation
        fields = (
            "id",
            "name",
            "enable",
            "start_time",
            "end_time",
            "display_automation_type",
        )


class AutomationDetailSerializer(WritableNestedModelSerializer):

    commands = CommandSerializer(many=True, required=False)
    display_automation_type = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_display_automation_type(obj):
        return obj.get_utomation_type_display()

    class Meta:
        model = Automation
        fields = (
            "id",
            "name",
            "enable",
            "start_time",
            "end_time",
            "commands",
            "conditions",
            "display_automation_type",
        )
