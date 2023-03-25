import json
from typing import List

import requests
from loguru import logger
from django.conf import settings
from requests.auth import HTTPBasicAuth


class EMQXApi:
    """
    emqx http api
    文档地址：https://www.emqx.io/docs/zh/v4.4/advanced/http-api.html
    """

    def __int__(
        self,
        url: str = settings.EMQX_HTTP_API_BASE_URL,
        username: str = settings.EMQX_HTTP_API_USERNAME,
        password: str = settings.EMQX_HTTP_API_PASSWORD,
    ):
        self.url = url
        self.username = username
        self.password = password

    def _auth(self):
        return HTTPBasicAuth(self.username, self.password)

    @staticmethod
    def _response(response: requests.Response) -> bool:
        if response.status_code == 200 and response.json().get("code") == 0:
            return True
        else:
            logger.info(response.text)
            return False

    def subscribe(self, clientid: str, topic: str = None, topics: str = None, qos: int = 0) -> bool:
        """
        订阅主题
        :param topic: 主题，与 topics 至少指定其中之一
        :param topics: 以 , 分割的多个主题，使用此字段能够同时订阅多个主题
        :param clientid: 客户端ID
        :param qos: QoS等级
        """
        if not topic and not topics:
            raise Exception("topic and topics can't be both None")
        url = f"{self.url}/api/v4/mqtt/subscribe"
        data = {"topic": topic, "clientid": clientid, topics: topics, "qos": qos}
        response = requests.post(url, data=data, auth=self._auth())
        return self._response(response)

    def subscribe_batch(self, sub_list: List[dict]) -> bool:
        """
        批量订阅主题
        :param sub_list: 订阅列表，内容同 subscribe
        :e.g [
            {"topic": "topic1", "qos": 0, "clientid": "client1"}，
            {"topics": "topic1,topic2", "qos": 0, "clientid": "client2"}
        ]
        """
        for sub in sub_list:
            if not sub.get("topic") and not sub.get("topics"):
                raise Exception("topic and topics can't be both None")
            if not sub.get("clientid"):
                raise Exception("clientid can't be None")
        url = f"{self.url}/api/v4/mqtt/subscribe_batch"
        data = json.dumps(sub_list)
        response = requests.post(url, data=data, auth=self._auth())
        return self._response(response)

    def publish(
        self,
        clientid: str,
        payload: str,
        topic: str = None,
        topics: str = None,
        qos: int = 0,
        properties: dict = None,
    ) -> bool:
        """
        发布消息
        :param clientid: 客户端ID
        :param payload: 消息内容
        :param topic: 主题，与 topics 至少指定其中之一
        :param topics: 以 , 分割的多个主题，使用此字段能够同时发布消息到多个主题
        :param qos: QoS等级
        :param properties: PUBLISH 消息里的 Property 字段
        """
        if not topic and not topics:
            raise Exception("topic and topics can't be both None")
        url = f"{self.url}/api/v4/mqtt/publish"
        data = {
            "clientid": clientid,
            "payload": payload,
            "topic": topic,
            topics: topics,
            "qos": qos,
            "properties": properties,
        }
        response = requests.post(url, data=data, auth=self._auth())
        return self._response(response)

    def publish_batch(self, pub_list: List[dict]) -> bool:
        """
        批量订阅主题
        :param pub_list: 订阅列表，内容同 publish
        :e.g [
            {"topic":"t1","payload":"p1","qos":1,"clientid":"c1","properties":{"user_properties": { "id": 10010}}，
            {"topics": "t2,t3","payload":"p2","qos":1,"clientid":"c2","properties":{"user_properties": { "id": 10011}}，
        ]
        """
        for pub in pub_list:
            if not pub.get("topic") and not pub.get("topics"):
                raise Exception("topic and topics can't be both None")
            if not pub.get("clientid") or not pub.get("payload"):
                raise Exception("clientid and payload can't be None")
        url = f"{self.url}/api/v4/mqtt/publish_batch"
        data = json.dumps(pub_list)
        response = requests.post(url, data=data, auth=self._auth())
        return self._response(response)
