from django.db import models
from django.contrib.auth.models import Group

from base.base_model import BaseModel


class GroupExtend(BaseModel):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = "auth_group_extend"
        verbose_name = "用户组扩展"

    def __str__(self):
        return f"group: {self.group.name}"
