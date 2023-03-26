from base.base_serializers import BaseModelSerializer
from control.models.command_log import CommandLog


class CommandLogSerializer(BaseModelSerializer):
    class Meta:
        model = CommandLog
        fields = "__all__"
