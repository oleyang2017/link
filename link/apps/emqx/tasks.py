from datetime import datetime

from celery import shared_task
from loguru import logger

from device.models.device import Device


@shared_task
def handle_client_status(request):
    client_id = request.get("clientid")
    action = request.get("action")
    device = Device.objects.filter(client_id=client_id).first()
    if device:
        device.last_connect_time = datetime.now()
        device.status = True if action == "client_connected" else False
        device.save()
    return


@shared_task
def handle_publish(request):
    logger.info(request)
    return


@shared_task
def handle_subscribe(request):
    logger.info(request)
    return
