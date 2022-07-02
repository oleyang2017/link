from services.database.db import db
from services.database.models import Device
from services.tasks.celery_app import celery_app


@celery_app.task
def change_device_status(request, status: bool):
    client_id = request.clientinfo.clientid
    device = db.session.query(Device).filter(Device.client_id == client_id).first()
    if device:
        device.status = status
        db.session.commit()
