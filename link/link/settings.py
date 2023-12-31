"""
Django settings for link project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import sys
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "*ahhox%k)*#to$q2ms)kuqkg^74b0bm90=%1#8d^fbt84&p85q"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "*",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "guardian",
    "cacheops",
    "django_filters",
    "emqx",
    "user",
    "device",
    "invite",
    "control",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "link.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "link.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASES = {
    "default": {
        "ENGINE": "timescale.db.backends.postgresql",
        "NAME": "link",
        "USER": "admin",
        "PASSWORD": "admin",
        "HOST": "link_pgsql",
        "PORT": "5432",
        "OPTIONS": {"client_encoding": "UTF8"},
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 设置自定义的User模型
AUTH_USER_MODEL = "user.UserProfile"

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%Y-%m-%d",
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

# 默认设置JWT有效期为7天
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=7),
}

# 微信小程序appid和secret
WX_APPID = "your wechat miniprogram appid"
WX_SECRET = "your wechat miniprogram secret"

# 每个用户注册设备数量限制，为None时无数量限制
MAX_DEVICE_NUM = None
# 每个设备数量最多可绑定的数据流限制
MAX_STREAM_NUM = None


CACHEOPS_REDIS = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
}

# CACHEOPS = {
#     'device.*': {'ops': 'all', 'timeout': 60*15},
# }


# Celery settings

CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"

CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"

CELERY_RESULT_SERIALIZER = "json"

CELERY_TASK_RESULT_EXPIRES = 60 * 60

CELERY_TASK_TIME_LIMIT = 5 * 60

CELERY_TIMEZONE = "Asia/Shanghai"

CELERY_IMPORTS = ("emqx.tasks",)


# EMQX配置

EMQX_HTTP_API_BASE_URL = "http://127.0.0.1:8081/api/v4"

EMQX_HTTP_API_USERNAME = "admin"
# 默认密码，首次登录修改密码后请修改此处
EMQX_HTTP_API_PASSWORD = "public"

EMQX_HTTP_API_CLIENT_ID = "$SYS"


# debug模式下开启debug_toolbar显示
if DEBUG:
    INTERNAL_IPS = ["127.0.0.1"]
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_COLLAPSED": True,
    }

try:
    from .local_settings import *
except ImportError:
    pass
