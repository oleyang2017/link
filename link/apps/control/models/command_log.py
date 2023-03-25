import uuid

from django.db import models


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
    automation_log = models.ForeignKey(
        "control.AutomationLog",
        null=True,
        blank=True,
        related_name="command_logs",
        verbose_name="自动化日志",
        on_delete=models.CASCADE,
        db_constraint=False,
        db_index=True,
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    payload = models.TextField(verbose_name="下发指令内容", blank=False, null=False)
    result = models.TextField(blank=True, default="", verbose_name="执行结果")
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    callback_time = models.DateTimeField(verbose_name="回调时间", null=True, blank=True)

    class Meta:
        db_table = "command_log"
        verbose_name = "指令发送日志"
        verbose_name_plural = verbose_name
