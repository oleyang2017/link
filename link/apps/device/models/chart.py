from django.db import models
from django.dispatch import receiver
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save, pre_delete

from base.base_model import BaseModel

from .stream import Stream


class Chart(BaseModel):
    """
    历史数据图表
    """

    chart_id = ShortUUIDField(
        db_index=True,
        unique=True,
    )
    device = models.ForeignKey(
        "device.Device",
        related_name="charts",
        null=True,
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    streams = models.ManyToManyField("device.Stream", related_name="charts", db_constraint=False)
    title = models.CharField(max_length=16, verbose_name="标题", null=True, blank=True)
    name = models.CharField(max_length=16, verbose_name="名称")
    theme = models.TextField(verbose_name="自定义主题", null=True, blank=True)
    option = models.JSONField(verbose_name="自定义配置", null=True, blank=True)
    sequence = models.IntegerField(verbose_name="顺序", default=0)

    class Meta:
        db_table = "chart"
        verbose_name = "历史数据图表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

# @receiver(post_save, sender=Stream, dispatch_uid="add_chart_stream")
# def add_chart_stream(sender, instance, **kwargs):
#     if kwargs.get("created"):
#         chart = Chart.objects.create(
#             device=instance.device,
#             title=instance.name,
#             create_user=instance.create_user,
#         )
#         chart.streams.add(instance)
#
#
# @receiver(pre_delete, sender=Stream, dispatch_uid="remove_chart_stream")
# def remove_chart_stream(sender, instance, **kwargs):
#     # 如果某个图表只绑定了即将删除的数据流，则同时删除该图表
#     for chart in instance.charts.all():
#         if chart.streams.count() == 1:
#             chart.deleted = True
#             chart.save()
