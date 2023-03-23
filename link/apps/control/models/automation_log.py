from django.db import models

from base.base_model import BaseModel


class AutomationLog(BaseModel):
    automation = models.ForeignKey(
        "control.Automation",
        null=False,
        blank=False,
        related_name="logs",
        verbose_name="自动化",
        on_delete=models.CASCADE,
        db_constraint=False,
        db_index=True,
    )
    reason = models.TextField(verbose_name="触发原因", blank=False, null=False)
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "automation_log"
        verbose_name = "自动化执行日志"
        verbose_name_plural = verbose_name
