from device.models.chart import Chart
from base.base_serializers import BaseModelSerializer


class ChartDetailSerializer(BaseModelSerializer):
    class Meta:
        model = Chart
        fields = ("id", "name", "created_time", "update_time", "theme", "option", "title")
        read_only_fields = ("id", "chart_id", "created_time", "update_time")

    def create(self, validated_data):
        validated_data["create_user"] = self.context["request"].user
        return super(ChartDetailSerializer, self).create(validated_data)
