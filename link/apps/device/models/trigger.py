from django.db import models
from django.conf import settings

from shortuuid.django_fields import ShortUUIDField


class Trigger(models.Model):
    # TODO: 要支持设备间的联动， 邮件通知， http请求
    TRIGGER_CHOICE = (
        ('email', '邮件通知'),
        ('url', '发送HTTP请求'),
        ('action', '执行动作'),
        ('action_item', '执行指令'),
    )
    CONDITION_CHOICE = (
        # 仅对数据流类型为int，float类型开放，符合对应运算符计算时触发
        ('<', '<'),
        ('<=', '<='),
        ('==', '=='),
        ('>', '>'),
        ('>=', '>='),
        # 仅对数据流为boolean类型开放
        ('true', 'true'),
        # 对非char的数据流开放，当数值发生变化时触发
        ('change', 'change'),
    )
    trigger_id = ShortUUIDField(db_index=True, unique=True,)
    device = models.ForeignKey('device.Device', related_name='triggers', verbose_name='设备', on_delete=models.CASCADE)
    stream = models.ForeignKey('device.Stream', related_name='triggers', verbose_name='数据流', on_delete=models.CASCADE)  # 对于
    # action = models.ForeignKey('action.Action', related_name='triggers', verbose_name='动作', null=True, blank=True, on_delete=models.DO_NOTHING)
    # action_item = models.ForeignKey('action.ActionItem', related_name='triggers', verbose_name='指令', null=True, blank=True, on_delete=models.DO_NOTHING)
    url = models.URLField(verbose_name='URL', blank=True, default='')
    condition = models.CharField(max_length=8, verbose_name='触发条件', choices=CONDITION_CHOICE, default='==')
    threshold_value = models.FloatField(verbose_name='阈值', default=0)
    trigger_type = models.CharField(max_length=12, verbose_name='触发类型', choices=TRIGGER_CHOICE, default='action_item')
    start_time = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_time = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name='启用')
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='triggers', verbose_name='创建人', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '触发器'
        verbose_name_plural = verbose_name


class TriggerLog(models.Model):
    trigger = models.ForeignKey(Trigger, related_name='logs', verbose_name='触发器详情', null=True, blank=True, on_delete=models.SET_NULL)
    device = models.ForeignKey('device.Device', related_name='trigger_logs', verbose_name='设备', on_delete=models.CASCADE)
    stream = models.ForeignKey('device.Stream', related_name='trigger_logs', verbose_name='数据流', on_delete=models.CASCADE)
    result = models.TextField(blank=True, default='', verbose_name='执行结果')
    success = models.BooleanField(default=False, verbose_name='是否成功')
    value = models.CharField(verbose_name='触发值', max_length=32)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '触发器日志'
        verbose_name_plural = verbose_name


