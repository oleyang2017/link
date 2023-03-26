from base.base_serializers import BaseModelSerializer
from control.models.action import Action


class ActionSerializer(BaseModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"
