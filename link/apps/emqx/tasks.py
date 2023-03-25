import json
from datetime import datetime

from loguru import logger

from celery import shared_task
from utils.convert import str_to_number
from emqx.models.data import EMQXData
from device.models.device import Device
from device.models.stream import Stream
from emqx.service.emqx_api import EMQXApi


@shared_task
def handle_client_status(request):
    # 处理设备上下线状态
    client_id = request.get("clientid")
    action = request.get("action")
    device = Device.objects.filter(client_id=client_id).first()
    if device:
        if action == "client_connected":
            handle_auto_subscribe.delay(device.id)
        device.last_connect_time = datetime.now()
        device.status = True if action == "client_connected" else False
        device.save()
    return


@shared_task
def handle_publish(request):
    # 处理publish消息
    logger.info(request)
    topic = request.get("topic")
    if topic == "$save":
        handle_save_data.delay(request)
    elif topic.startswith("$resp"):
        handle_resp_data.delay(request)

    return


@shared_task
def handle_subscribe(request):
    # 处理subscribe消息
    logger.info(request)
    return


@shared_task
def handle_auto_subscribe(device_id: int):
    # 处理自动订阅消息
    emqx_api = EMQXApi()
    device = Device.objects.filter(id=device_id).first()
    if not device:
        return
    commands = device.commands.all().values("command_id")
    topics = ",".join([f"$cmd/{i['command_id']}" for i in commands])
    if topics:
        emqx_api.subscribe(clientid=device.client_id, topics=topics)
    return


@shared_task
def handle_save_data(request):
    # 保存数据
    client_id = request.get("from_client_id")
    payload = request.get("payload")
    node = request.get("node")
    timestamp = request.get("timestamp")
    try:
        payload = json.loads(payload)
        if not isinstance(payload, dict):
            logger.error(f"消息格式不正确: {payload}")
            return
        record = []
        streams = Stream.objects.filter(
            name__in=payload.keys(), device__client_id=client_id
        ).values("name", "id")
        stream_map = {i["name"]: i["id"] for i in streams}
        for k, v in payload.items():
            try:
                if k in stream_map:
                    record.append(
                        EMQXData(
                            client_id=client_id,
                            stream_id=stream_map[k],
                            payload=str_to_number(v),
                            node=node,
                            timestamp=timestamp,
                        )
                    )
            except ValueError as e:
                logger.error(e)
        EMQXData.objects.bulk_create(record)
        return
    except json.JSONDecodeError:
        logger.error(f"消息格式不正确: {payload}")
        return


@shared_task
def handle_resp_data(request):
    pass
