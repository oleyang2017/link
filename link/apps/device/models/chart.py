from django.db import models

from base.base_model import BaseModel
from utils.fields import ShortUUIDField


class Chart(BaseModel):
    """
    历史数据图表
    """
    device = models.ForeignKey(
        "device.Device",
        related_name="charts",
        null=True,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    streams = models.ManyToManyField("device.Stream", related_name="charts", db_constraint=False)
    title = models.CharField(max_length=16, verbose_name="标题", null=True, blank=True)
    name = models.CharField(max_length=16, verbose_name="名称", null=True, blank=True)
    theme = models.TextField(verbose_name="自定义主题", null=True, blank=True)
    option = models.JSONField(verbose_name="自定义配置", null=True, blank=True)
    sequence = models.IntegerField(verbose_name="顺序", default=0)

    class Meta:
        db_table = "chart"
        verbose_name = "历史数据图表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
