from django.db import models
from django.conf import settings

from utils.field_extend import ShortUUIDField


class Action(models.Model):
    """
    动作
    """
    id = ShortUUIDField(db_index=True, primary_key=True)
    show = models.BooleanField(default=True, verbose_name='首页显示')
    name = models.CharField(max_length=8, verbose_name='动作名称')
    device = models.ForeignKey('device.Device', related_name='actions', verbose_name='所属设备', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '动作'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name if self.name else self.device.name

    def send(self, content, operator, log=True):
        """
        执行动作
        :param content: 消息类容
        :param operator: 操作人
        :param log: 是否需要记录日志
        :return:
        """
        # TODO: 放到消息队列中执行，使用webAPI 或者 MQTT client
        if log:
            ActionLog.objects.create({
                'device': self.device,
                'content': content,
                'operator': operator
            })


class ActionItem(models.Model):

    QOS_CHOICE = (
        (0, '0'),
        (1, '1'),
        (2, '2')
    )
    ACTION_TYPE_CHOICE = (
        ('none', '普通'),
        ('button', '按钮'),
        ('switch', '开关'),
        ('slider', '滑块'),
    )
    SIZE_CHOICE = (
        ('small', '小号'),
        ('default', '默认'),
        ('lager', '大号')
    )
    id = ShortUUIDField(db_index=True, primary_key=True)
    action = models.ForeignKey(Action, related_name='items', on_delete=models.CASCADE)
    device = models.ForeignKey('device.Device', related_name='action_items', verbose_name='所属设备', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=8, blank=True, verbose_name='指令名称')
    action_type = models.CharField(max_length=8, choices=ACTION_TYPE_CHOICE, default='button', verbose_name='动作类型')
    topic = models.CharField(max_length=32, verbose_name='topic')
    qos = models.IntegerField(choices=QOS_CHOICE, default=0, verbose_name='qos')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # button
    content = models.CharField(max_length=128, blank=True, verbose_name='指令内容')
    # switch
    last_content = models.CharField(max_length=128, blank=True, verbose_name='记录值')
    on_content = models.CharField(max_length=128, blank=True, verbose_name='打开值')
    off_content = models.CharField(max_length=128, blank=True, verbose_name='关闭值')
    # slider
    last_value = models.IntegerField(default=0, blank=True, verbose_name='记录值')
    max_value = models.IntegerField(default=100, blank=True, verbose_name='最大值')
    min_value = models.IntegerField(default=0, blank=True, verbose_name='最小值')
    setup = models.IntegerField(default=1, blank=True, verbose_name='步长')

    def get_default_topic(self):
        pass

    class Meta:
        verbose_name = '指令内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ActionLog(models.Model):
    """
    动作日志
    """
    device = models.ForeignKey('device.Device', related_name='action_logs', verbose_name='接收设备', on_delete=models.CASCADE)
    operator = models.CharField(max_length=32, verbose_name='操作人', default='')
    action = models.ForeignKey(Action, related_name="logs", verbose_name='动作详情', null=True, blank=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='执行时间')
    content = models.CharField(max_length=32, default='', blank=True, verbose_name='指令内容')
    result = models.TextField(blank=True, default='', verbose_name='执行结果')
    success = models.BooleanField(default=True, verbose_name='是否成功')

    class Meta:
        verbose_name = '设备日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.device.name
