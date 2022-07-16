from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from base.base_viewsets import BaseModelViewSet
from device.models.stream import Stream
from device.serializers.stream import StreamSerializer


class StreamViewSet(BaseModelViewSet):
    serializer_class = StreamSerializer
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ["device", "name", "data_type", "show"]
    search_fields = ["device"]
    queryset = Stream.objects
