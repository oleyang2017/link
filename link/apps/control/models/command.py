from django.db import models

from utils.fields import ShortUUIDField
from base.base_model import BaseModel


def handle_command_delete(collector, field, sub_objs, using):
    """
    处理删除如果删除中间节点，需要将子节点的父节点指向当前节点的父节点
    """
    command = collector.origin
    next_commands = sub_objs.all()
    if command.previous and next_commands:
        command.previous.next.set(next_commands)


class Command(BaseModel):
    automation = models.ForeignKey(
        "control.Automation",
        null=True,
        blank=True,
        related_name="commands",
        verbose_name="所属自动化",
        on_delete=models.CASCADE,
        db_index=True,
        db_constraint=False,
    )
    action = models.ForeignKey(
        "control.Action",
        null=True,
        blank=True,
        related_name="commands",
        verbose_name="所属动作",
        on_delete=models.CASCADE,
        db_index=True,
        db_constraint=False,
    )
    previous = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        verbose_name="上一条指令",
        related_name="next",
        on_delete=handle_command_delete,
        db_constraint=False,
    )
    device = models.ManyToManyField(
        "device.Device",
        null=True,
        blank=True,
        related_name="commands",
        verbose_name="指定的设备",
        db_constraint=False,
    )
    command_id = ShortUUIDField(verbose_name="指令ID")
    content = models.CharField(max_length=256, verbose_name="内容", blank=False, null=False)
    sleep = models.IntegerField(default=0, verbose_name="执行下next指令的延时延时")
    topic = models.CharField(max_length=256, verbose_name="topic", blank=False, null=False)

    class Meta:
        db_table = "command"
        verbose_name = "指令"
        verbose_name_plural = verbose_name
