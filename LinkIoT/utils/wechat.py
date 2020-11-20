import json

import requests
from requests.exceptions import Timeout
from django.conf import settings
from rest_framework import exceptions


def code2openid(code: str) -> str:
    """
    将code转换成openid
    :param code: 小程序登录code
    :return: openid
    """
    payload = {'appid': settings.WX_APPID,
               'secret': settings.WX_SECRET,
               'js_code': code,
               'grant_type': 'authorization_code'}
    request_url = "https://api.weixin.qq.com/sns/jscode2session"
    try:
        recv = requests.get(request_url, params=payload, timeout=5)
    except Timeout:
        raise exceptions.APIException(detail='登陆超时', code=500)
    if recv.status_code == 200:
        recv = json.loads(recv.text)
        if recv.get('openid'):
            return recv['openid']
        else:
            raise exceptions.APIException(detail='登录失败', code=500)
    else:
        raise exceptions.APIException(detail='登录失败', code=500)
