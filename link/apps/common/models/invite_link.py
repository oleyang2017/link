from datetime import datetime

from django.db import models
from shortuuid.django_fields import ShortUUIDField
from rest_framework.exceptions import ValidationError

from base.base_model import BaseModel


class InviteLink(BaseModel):
    """邀请连接，用于添加协作人，或者组成员"""

    INVITE_TYPE_CHOICES = (
        ("device", "设备"),
        ("group", "群组"),
    )

    code = ShortUUIDField(length=8, verbose_name="邀请码", unique=True, db_index=True)
    end_time = models.DateTimeField(verbose_name="邀请结束时间", null=True, blank=True)
    count = models.IntegerField(verbose_name="邀请人数", default=0)
    invite_type = models.CharField(choices=INVITE_TYPE_CHOICES, max_length=16, verbose_name="邀请类型")
    object_id = models.BigIntegerField(verbose_name="对象ID")
    permissions = models.JSONField(verbose_name="权限", default=list)
    enable = models.BooleanField(default=True, verbose_name="开启")

    class Meta:
        db_table = "invite_link"
        verbose_name = "邀请连接"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"邀请码: {self.code}"

    def check_can_join(self, operation, user):
        from common.models.invite_record import InviteRecord

        now = datetime.now()
        if operation == "accept":
            if self.end_time and self.end_time < now:
                raise ValidationError("邀请链接已过期")
            if self.count and self.count <= self.invite_records.filter(operation="accept").count():
                raise ValidationError("邀请人数已达上限")
            if not self.enable:
                raise ValidationError("邀请链接已不可使用")
        record = InviteRecord.objects.filter(create_user=user, invite_link=self).first()
        if record:
            raise ValidationError(f"你已{record.get_operation_display()}")
        if user == self.create_user:
            raise ValidationError("无法执行操作")
