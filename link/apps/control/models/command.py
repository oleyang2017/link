from django.db import models

from base.base_model import BaseModel


class Command(BaseModel):
    QOS_CHOICE = ((0, "0"), (1, "1"), (2, "2"))
    device = models.ForeignKey(
        "device.Device",
        null=True,
        blank=True,
        related_name="commands",
        verbose_name="所属设备",
        on_delete=models.SET_NULL,
        db_index=True,
        db_constraint=False
    )
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
    next = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        verbose_name="next指令",
        related_name="next_commands",
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    partner = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        verbose_name="同级指令",
        related_name="partner_commands",
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    content = models.CharField(max_length=256, verbose_name="内容", blank=False, null=False)
    callback = models.BooleanField(default=False, verbose_name="是否需要等待回调后再执行next指令")
    sleep = models.IntegerField(default=0, verbose_name="执行下next指令的延时延时")
    topic = models.CharField(max_length=256, verbose_name="topic", blank=False, null=False)
    qos = models.IntegerField(choices=QOS_CHOICE, default=0, verbose_name="qos")

    class Meta:
        verbose_name = "指令"
        verbose_name_plural = verbose_name
