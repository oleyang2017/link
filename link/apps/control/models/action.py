from django.db import models

from base.base_model import BaseModel


class Action(BaseModel):
    show = models.BooleanField(default=True, verbose_name="首页显示")
    name = models.CharField(max_length=8, verbose_name="名称")
    device = models.ForeignKey(
        "device.Device",
        related_name="actions",
        verbose_name="所属设备",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    save_value = models.BooleanField(default=False, verbose_name="是否保存值")
    style = models.JSONField(verbose_name="控件样式", null=True, blank=True)

    class Meta:
        verbose_name = "动作"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
