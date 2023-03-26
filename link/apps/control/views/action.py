from base.base_viewsets import BaseModelViewSet
from control.models.action import Action
from control.serializers.action import ActionSerializer


class ActionViewSet(BaseModelViewSet):
    lookup_field = "id"
    serializer_class = ActionSerializer
    queryset = Action.objects
