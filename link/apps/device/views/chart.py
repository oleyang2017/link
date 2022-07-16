from datetime import datetime, timedelta

from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from base.base_viewsets import BaseModelViewSet
from device.models.chart import Chart
from device.serializers.chart import ChartSerializer


class ChartViewSet(BaseModelViewSet):
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ["device", "name"]
    ordering_fields = ["sequence", "-created_time"]
    ordering = ["sequence", "-created_time"]
    queryset = Chart.objects
    serializer_class = ChartSerializer

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)

    @action(methods=["get"], detail=True)
    def data(self, request, *args, **kwargs):
        """
        获取图表数据
        """
        start_time = self.request.query_params.get("start_time", datetime.now() + timedelta(days=7))
        end_time = self.request.query_params.get("end_time", datetime.now())
        # TODO: 从数据模型中取出前端所需要的dataset
