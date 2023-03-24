from datetime import datetime

from celery import shared_task
from loguru import logger

from device.models.device import Device
from emqx.service.emqx_api import EMQXApi


@shared_task
def handle_client_status(request):
    # 处理设备上下线状态
    client_id = request.get("clientid")
    action = request.get("action")
    device = Device.objects.filter(client_id=client_id).first()
    if device:
        if action == "client_connected":
            handle_auto_subscribe.delay(device)
        device.last_connect_time = datetime.now()
        device.status = True if action == "client_connected" else False
        device.save()
    return


@shared_task
def handle_publish(request):
    # 处理publish消息
    logger.info(request)
    return


@shared_task
def handle_subscribe(request):
    # 处理subscribe消息
    logger.info(request)
    return


@shared_task
def handle_auto_subscribe(device: Device):
    # 处理自动订阅消息
    emqx_api = EMQXApi()
    commands = device.commands.all().values("command_id")
    topics = ",".join([f"$cmd/{i['command_id']}" for i in commands])
    emqx_api.subscribe(clientid=device.client_id, topics=topics)
    return
