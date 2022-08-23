from rest_framework.filters import OrderingFilter
from guardian.shortcuts import assign_perm, get_user_perms, get_objects_for_user
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from base.base_viewsets import BaseModelViewSet
from device.models.stream import Stream
from device.models.device import Device
from device.serializers.stream import StreamSerializer


class StreamViewSet(BaseModelViewSet):
    serializer_class = StreamSerializer
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ["device", "name", "data_type", "show"]
    search_fields = ["device"]

    def get_queryset(self):
        device_objets = get_objects_for_user(self.request.user, perms="view_device", klass=Device)
        print(device_objets)
        queryset = device_objets.streams
        queryset += Stream.objects.filter(create_user=self.request.user)
        # if self.request.query_params.get("only_creator", False):
        #     q_set = q_set.filter(create_user=self.request.user)
        return queryset

    def perform_update(self, serializer):
        if not self.request.user.has_perm("change_device", serializer.instance.device):
            raise PermissionDenied("你没有修改权限")
        return super(StreamViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if not self.request.user.has_perm("delete_device", instance.device):
            raise PermissionDenied("你没有删除权限")
        return super(StreamViewSet, self).perform_destroy(instance)

    # def perform_create(self, serializer):
    #     print(serializer)
    #     print(serializer.data)
    #     if not self.request.user.has_perm("change_device", serializer.data["device"]):
    #         raise PermissionDenied("你没有添加权限")
    #     return super(StreamViewSet, self).perform_create(serializer)
