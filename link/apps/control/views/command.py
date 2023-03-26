from base.base_viewsets import BaseModelViewSet
from control.models.command import Command
from control.serializers.command import CommandSerializer


class CommandViewSet(BaseModelViewSet):
    lookup_field = "id"
    serializer_class = CommandSerializer
    filterset_fields = ["automation", "action"]
    queryset = Command.objects
