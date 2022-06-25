from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户信息
    """

    GENDER_CHOICES = (("0", "未知"), ("1", "男"), ("2", "女"))
    mobile = models.CharField(verbose_name="手机号", max_length=20, unique=True, blank=True, null=True)
    wx_open_id = models.CharField(
        verbose_name="wx_openid", max_length=64, default="", blank=True, db_index=True
    )
    gender = models.CharField(verbose_name="性别", max_length=1, choices=GENDER_CHOICES, default="1")
    desc = models.TextField(verbose_name="个人介绍", blank=True, default="")
    avatar = models.ImageField(verbose_name="头像", upload_to="avatar/", blank=True, null=True)
    avatar_url = models.URLField(verbose_name=" 微信头像", blank=True, null=True)
    address = models.CharField(verbose_name="地址", max_length=128, default="", blank=True)
    create_time = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
