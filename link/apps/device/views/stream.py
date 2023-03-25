from django.db.models import Q
from guardian.shortcuts import get_objects_for_user
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from base.base_viewsets import BaseModelViewSet
from device.models.device import Device
from device.models.stream import Stream
from device.serializers.stream import (
    StreamListSerializer,
    StreamDetailSerializer,
    StreamCreateOrUpdateSerializer,
)


class StreamViewSet(BaseModelViewSet):
    serializer_class = StreamListSerializer
    lookup_field = "id"
    filterset_fields = ["device", "name", "data_type", "show"]
    search_fields = ["device"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return StreamListSerializer
        else:
            return StreamCreateOrUpdateSerializer

    def get_queryset(self):
        device_objets = get_objects_for_user(self.request.user, perms="view_device", klass=Device)
        return Stream.objects.filter(Q(device__in=device_objets) | Q(create_user=self.request.user))

    def perform_update(self, serializer):
        if not self.request.user.has_perm("change_device", serializer.instance.device):
            raise PermissionDenied("你没有修改权限")
        return super(StreamViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if not self.request.user.has_perm("delete_device", instance.device):
            raise PermissionDenied("你没有删除权限")
        return super(StreamViewSet, self).perform_destroy(instance)

    def perform_create(self, serializer):
        device_id = self.request.data.get("device")
        device = Device.objects.filter(id=device_id).first()
        if not self.request.user.has_perm("change_device", device):
            raise PermissionDenied("你没有添加权限")
        return super(StreamViewSet, self).perform_create(serializer)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StreamDetailSerializer(instance, context={"request": request})
        return Response(serializer.data)
