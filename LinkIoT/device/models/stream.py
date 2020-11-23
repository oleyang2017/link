from django.db import models
from django.conf import settings

from utils.field_extend import ShortUUIDField


class Stream(models.Model):
    """
    数据流
    """
    QOS_CHOICE = (
        (0, '0'),
        (1, '1'),
        (2, '2'),
    )
    DATA_TYPE_CHOICE = (
        ('int', '整型（int）'),
        ('json', 'JSON（json）'),
        ('float', '浮点型（float）'),
        ('bool', '布尔型（bool）'),
        ('char', '字符型（char）'),
    )
    name = models.CharField(max_length=16, verbose_name='名称')
    device = models.ForeignKey('device.Device', related_name='streams', verbose_name='所属设备', on_delete=models.CASCADE)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='streams', verbose_name='用户', on_delete=models.CASCADE)
    stream_id = ShortUUIDField(db_index=True, unique=True, verbose_name='数据流ID')
    unit = models.CharField(max_length=8,  blank=True, default='', verbose_name='单位')
    qos = models.IntegerField(choices=QOS_CHOICE, default=0, verbose_name='Qos')
    data_type = models.CharField(max_length=8, default='int', choices=DATA_TYPE_CHOICE, verbose_name='数据类型')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '数据流'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


