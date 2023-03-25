from django.db import models

from base.base_model import BaseModel


class Automation(BaseModel):
    AUTOMATION_TYPE_CHOICE = (
        ("date", "指定时间"),
        ("interval", "间隔时间"),
        ("cron", "定时任务"),
        ("stream", "数据流"),
    )
    automation_type = models.CharField(
        max_length=12,
        verbose_name="自动化类型",
        choices=AUTOMATION_TYPE_CHOICE,
        blank=False,
        null=False,
    )
    name = models.CharField(max_length=16, verbose_name="名称", blank=False, null=False)
    conditions = models.JSONField(verbose_name="条件", blank=False, null=False)
    enable = models.BooleanField(default=True, verbose_name="启用")
    start_time = models.DateTimeField(verbose_name="开始时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="结束时间", null=True, blank=True)

    class Meta:
        db_table = "automation"
        verbose_name = "自动化"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
