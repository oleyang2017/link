from rest_framework import viewsets
from django.db.models.query import QuerySet


class BaseModelViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
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

    # 由于微信小程序不支持patch方法，所以这里默认部分更新
    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        return super(BaseModelViewSet, self).get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(create_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(last_update_user=self.request.user)
