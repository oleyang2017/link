from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from device.models import Device, Stream


class EMQXAcl(models.Model):
    # EMQ权限控制表
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


@receiver(post_save, sender=Device, dispatch_uid="add_acl_device")
def add_acl_device(sender, instance, **kwargs):
    if kwargs.get("created"):
        EMQXAcl.objects.create(
            allow=1,
            clientid=instance.client_id,
            access=1,
            topic=f"device/{instance.client_id}/#",
        )


@receiver(post_delete, sender=Device, dispatch_uid="remove_acl_device")
def remove_acl_device(sender, instance, **kwargs):
    EMQXAcl.objects.filter(topic=f"device/{instance.client_id}/#").delete()


@receiver(post_save, sender=Stream, dispatch_uid="add_acl_stream")
def add_acl_stream(sender, instance, **kwargs):
    if kwargs.get("created"):
        EMQXAcl.objects.create(
            allow=1,
            clientid=instance.device.client_id,
            access=3,
            topic=f"device/{instance.device.client_id}/{instance.stream_id}",
        )


@receiver(post_delete, sender=Stream, dispatch_uid="remove_acl_stream")
def remove_acl_stream(sender, instance, **kwargs):
    EMQXAcl.objects.filter(
        topic=f"device/{instance.device.client_id}/{instance.stream_id}"
    ).delete()
