from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from base.base_viewsets import BaseModelViewSet
from device.models.trigger import Trigger
from device.serializers.trigger import TriggerSerializer


class TriggerViewSet(BaseModelViewSet):
    serializer_class = TriggerSerializer
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ("device", "stream")
    queryset = Trigger.objects
