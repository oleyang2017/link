from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter


class BaseModelViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ["created_time"]
    ordering = ["-created_time"]

    def get_queryset(self):
        queryset = super(BaseModelViewSet, self).get_queryset()
        if isinstance(queryset, QuerySet):
            queryset = queryset.filter(create_user=self.request.user.id).all()
        return queryset.filter(create_user=self.request.user.id)

    def get_raw_queryset(self):
        queryset = super(BaseModelViewSet, self).get_queryset()
        return queryset

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)

    # 由于微信小程序不支持patch方法，所以这里默认部分更新
    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        return super(BaseModelViewSet, self).get_serializer(*args, **kwargs)
