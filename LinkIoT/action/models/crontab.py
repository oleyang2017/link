from django.db import models


class CronTab(models.Model):
    CRON_TYPE_CHOICE = (
        ('click', '点击'),
        ('click', '点击'),
        ('click', '点击'),
    )
    cron_type = models.CharField(max_length=8, choices=CRON_TYPE_CHOICE, default='click', verbose_name='任务类型')


