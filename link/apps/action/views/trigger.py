from base.base_viewsets import BaseModelViewSet
from action.models.trigger import Trigger
from action.serializers.trigger import TriggerSerializer


class TriggerViewSet(BaseModelViewSet):
    serializer_class = TriggerSerializer
    lookup_field = "id"
    filter_fields = ("device", "stream")
    queryset = Trigger.objects
