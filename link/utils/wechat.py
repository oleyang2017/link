import json

import requests
from django.conf import settings
from requests.exceptions import Timeout
from rest_framework import exceptions


def code2openid(code: str) -> str:
    """
    将code转换成openid
    :param code: 小程序登录code
    :return: openid
    """
    payload = {
        "appid": settings.WX_APPID,
        "secret": settings.WX_SECRET,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    request_url = "https://api.weixin.qq.com/sns/jscode2session"
    try:
        rec = requests.get(request_url, params=payload, timeout=5)
    except Timeout:
        raise exceptions.APIException(detail="登陆超时", code=500)
    if rec.status_code == 200:
        rec = json.loads(rec.text)
        if rec.get("openid"):
            return rec["openid"]
        else:
            raise exceptions.APIException(detail="登录失败", code=500)
    else:
        raise exceptions.APIException(detail="登录失败", code=500)
