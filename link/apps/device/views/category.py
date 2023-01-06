from rest_framework.response import Response
from rest_framework.decorators import action

from base.base_viewsets import BaseModelViewSet
from device.models.category import DeviceCategory
from device.serializers.category import DeviceCategorySerializer


class CategoryViewSet(BaseModelViewSet):
    serializer_class = DeviceCategorySerializer
    lookup_field = "id"
    ordering_fields = ["sequence", "created_time"]
    ordering = ["sequence", "-created_time"]
    queryset = DeviceCategory.objects

    @action(methods=["put"], detail=False)
    def sort(self, request, *args, **kwargs):
        for cid in request.data:
            category = DeviceCategory.objects.filter(id=cid, create_user=request.user).first()
            if category:
                category.sequence = request.data[cid]
                category.save()
        return Response({})
