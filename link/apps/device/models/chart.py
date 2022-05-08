from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, post_init

from .stream import Stream
from shortuuid.django_fields import ShortUUIDField


class Chart(models.Model):
    """
    历史数据图表
    """
    chart_id = ShortUUIDField(db_index=True, unique=True,)
    device = models.ForeignKey('device.Device', related_name='charts', on_delete=models.CASCADE)
    streams = models.ManyToManyField('device.Stream', related_name='charts')
    title = models.CharField(max_length=16, verbose_name='标题')
    is_half = models.BooleanField(default=False, verbose_name='半屏显示')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='charts', verbose_name='创建人', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '历史数据图表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


@receiver(post_save, sender=Stream, dispatch_uid='add_chart_stream')
def add_chart_stream(sender, instance, **kwargs):
    if kwargs.get('created'):
        chart = Chart.objects.create(device=instance.device, title=instance.name, create_user=instance.create_user)
        chart.streams.add(instance)


@receiver(pre_delete, sender=Stream, dispatch_uid='remove_chart_stream')
def remove_chart_stream(sender, instance, **kwargs):
    # 如果某个图表只绑定了即将删除的数据流，则同时删除该图表
    for chart in instance.charts.all():
        if chart.streams.count() == 1:
            chart.delete()
