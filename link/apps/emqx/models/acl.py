from django.db import models


class EMQXAcl(models.Model):
    # EMQX权限控制表
    ACCESS_CHOICE = (
        (1, "可订阅"),
        (2, "可发布"),
        (3, "两者皆可"),
    )
    allow = models.IntegerField(blank=True, default=1)  # 1:允许, 0:禁止
    ipaddr = models.CharField(max_length=60, blank=True, default="")  # ip地址
    username = models.CharField(max_length=100, blank=True, default="")  # 用户名
    clientid = models.CharField(max_length=100, blank=True, default="")  # 设备名
    access = models.IntegerField(choices=ACCESS_CHOICE, default=2)  # 1：可订阅  2：可发布  3 两者皆可
    topic = models.CharField(max_length=100)  # 主题名

    class Meta:
        db_table = "emqx_acl"
        verbose_name = "EMQX权限控制表"
        verbose_name_plural = verbose_name
