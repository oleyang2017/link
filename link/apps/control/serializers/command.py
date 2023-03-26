from base.base_serializers import BaseModelSerializer
from control.models.command import Command


class CommandSerializer(BaseModelSerializer):
    class Meta:
        model = Command
        fields = "__all__"
