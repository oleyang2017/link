from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户信息
    """

    GENDER_CHOICES = (("0", "未知"), ("1", "男"), ("2", "女"))
    username = ShortUUIDField(prefix="wx_", max_length=128, length=16, unique=True)
    nickname = models.CharField(verbose_name="昵称", max_length=12, default="微信用户")
    mobile = models.CharField(verbose_name="手机号", max_length=20, unique=True, blank=True, null=True)
    wx_open_id = models.CharField(
        verbose_name="wx_openid", max_length=64, default="", blank=True, db_index=True
    )
    wx_union_id = models.CharField(
        verbose_name="wx_union_id", max_length=64, default="", blank=True, db_index=True
    )
    gender = models.CharField(verbose_name="性别", max_length=1, choices=GENDER_CHOICES, default="0")
    desc = models.TextField(verbose_name="个人介绍", blank=True, default="")
    avatar = models.ImageField(verbose_name="头像", upload_to="images/avatar", blank=True, null=True)
    avatar_url = models.URLField(verbose_name="头像", blank=True, null=True)
    address = models.CharField(verbose_name="地址", max_length=128, default="", blank=True)
    # 目前没有打算通过用户名密码的方式登录，只有微信授权登录的方式，增加access_token方便以后不使用微信授权直接换取jwt
    access_token = ShortUUIDField(length=24, verbose_name="access_token", unique=True)
    created_time = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)

    class Meta(AbstractUser.Meta):
        db_table = "auth_user"
        swappable = "AUTH_USER_MODEL"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"user: {self.username}"
