from django.db import models
from shortuuid.django_fields import ShortUUIDField
from base.base_model import BaseModel


class InviteLink(BaseModel):
    """邀请连接，用于添加协作人，或者组成员"""

    INVITE_TYPE_CHOICES = (
        ("device", "设备"),
        ("group", "群组"),
    )

    code = ShortUUIDField(length=8, verbose_name="邀请码", unique=True, db_index=True)
    end_time = models.DateTimeField(verbose_name="邀请结束时间")
    count = models.IntegerField(verbose_name="邀请人数", default=0)
    invite_type = models.CharField(choices=INVITE_TYPE_CHOICES, max_length=16, verbose_name="邀请类型")
    object_id = models.BigIntegerField(verbose_name="对象ID")
    permissions = models.JSONField(verbose_name="权限")

    class Meta:
        db_table = "invite_link"
        verbose_name = "邀请连接"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"邀请码: {self.code}"
