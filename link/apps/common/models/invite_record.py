from django.db import models

from base.base_model import BaseModel
from common.models.invite_link import InviteLink


class InviteRecord(BaseModel):
    """邀请记录"""

    OPERATION_CHOICES = (
        ("accept", "接受邀请"),
        ("reject", "拒绝邀请"),
    )
    code = models.CharField(max_length=8, verbose_name="邀请码")
    invite_link = models.ForeignKey(
        InviteLink,
        related_name="invite_records",
        on_delete=models.CASCADE,
        db_constraint=False,
        verbose_name="邀请链接",
    )
    object_id = models.BigIntegerField(verbose_name="对象ID")
    permissions = models.JSONField(verbose_name="权限", default=list)
    operation = models.CharField(
        choices=OPERATION_CHOICES, max_length=16, verbose_name="邀请类型", null=False
    )

    class Meta:
        db_table = "invite_record"
        verbose_name = "邀请记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"邀请记录: {self.create_user} - {self.code} - {self.operation}"
