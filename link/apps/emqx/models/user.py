from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from utils.shortuuid import ShortUUIDField


class EMQXUser(models.Model):
    # EMQX用户表

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="emqx_user",
        verbose_name="创建人",
        on_delete=models.CASCADE,
        db_constraint=False,
    )
    username = ShortUUIDField()
    password = ShortUUIDField()

    class Meta:
        db_table = "emqx_user"
        verbose_name = "EMQX用户表"


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="add_emqx_user")
def add_emqx_user(sender, instance, **kwargs):
    if kwargs.get("created"):
        EMQXUser.objects.create(user=instance)


@receiver(post_delete, sender=settings.AUTH_USER_MODEL, dispatch_uid="remove_emqx_user")
def add_emqx_user(sender, instance, **kwargs):
    EMQXUser.objects.filter(user=instance).delete()
