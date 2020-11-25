from django.db import models
from django.conf import settings

from utils.field_extend import ShortUUIDField
from utils.default_chart_style import get_default_chart_style


class Chart(models.Model):
    """
    历史数据图表
    """
    id = ShortUUIDField(db_index=True, primary_key=True)
    device = models.ForeignKey('device.Device', related_name='charts', on_delete=models.CASCADE)
    streams = models.ManyToManyField('device.Stream', related_name='charts')
    title = models.CharField(max_length=16, verbose_name='标题')
    is_half = models.BooleanField(default=False, verbose_name='半屏显示')
    style = models.JSONField(default=get_default_chart_style, verbose_name='图表样式')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='charts', verbose_name='用户',
                                    on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '历史数据图表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
