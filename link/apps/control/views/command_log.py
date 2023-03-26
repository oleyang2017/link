from base.base_viewsets import BaseModelViewSet
from control.models.command_log import CommandLog
from control.serializers.command_log import CommandLogSerializer


class CommandLogViewSet(BaseModelViewSet):
    lookup_field = "id"
    serializer_class = CommandLogSerializer
    queryset = CommandLog.objects
