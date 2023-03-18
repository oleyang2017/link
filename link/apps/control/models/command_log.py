from django.db import models
from django.conf import settings


class CommandLog(models.Model):
    command = models.ForeignKey(
        "control.Command",
        null=True,
        blank=True,
        related_name="logs",
        verbose_name="指令",
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    content = models.TextField(verbose_name="触发原因", blank=False, null=False)
    result = models.TextField(blank=True, default="", verbose_name="执行结果")
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "command_log"
        verbose_name = "指令发送日志"
        verbose_name_plural = verbose_name
