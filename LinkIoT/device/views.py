from datetime import datetime, timedelta

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *


class BaseModelViewSet(viewsets.ModelViewSet):

    def get_serializer_context(self):
        ret = super(BaseModelViewSet, self).get_serializer_context()
        ret['user'] = self.request.user
        return ret

    # 由于微信小程序不支持patch方法，所以这里默认部分更新
    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(BaseModelViewSet, self).get_serializer(*args, **kwargs)


class DeviceViewSet(BaseModelViewSet):

    serializer_class = DeviceSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('category',)
    ordering_fields = ('sequence',)

    def get_queryset(self):
        return self.request.user.devices

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeviceSerializer
        else:
            return DeviceDetailSerializer

    @action(methods=['get'], detail=True)
    def streams(self, request, *args, **kwargs):
        device = self.get_object()
        serializer = StreamSerializer(device.streams, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DeviceDetailSerializer(instance)
        return Response(serializer.data)


class CategoryViewSet(BaseModelViewSet):

    serializer_class = DeviceCategorySerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('sequence',)

    def get_queryset(self):
        return self.request.user.device_categories

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)


class StreamViewSet(BaseModelViewSet):
    serializer_class = StreamSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('device',)

    def get_queryset(self):
        return self.request.user.streams

    def get_serializer_context(self):
        ret = super(StreamViewSet, self).get_serializer_context()
        ret['user'] = self.request.user
        return ret

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)


class ChartViewSet(BaseModelViewSet):
    serializer_class = ChartSerializer
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('device',)

    def get_queryset(self):
        return self.request.user.charts

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)

    @action(methods=['get'], detail=True)
    def data(self, request, *args, **kwargs):
        """
        获取图表数据
        """
        start_time = self.request.query_params.get('start_time', datetime.now() + timedelta(days=7))
        end_time = self.request.query_params.get('end_time', datetime.now())
        # TODO: 从数据模型中取出前端所需要的dataset

