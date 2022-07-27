from datetime import datetime

from loguru import logger
from services.database.db import db
from services.database.models import Stream, EmqxData
from services.tasks.celery_app import celery_app


@celery_app.task
def on_published(request):
    logger.info(request)
    save_emqx_data.delay(request)


@celery_app.task
def save_emqx_data(request):
    node = request["message"]["node"]
    msg_id = request["message"]["id"]
    topic = request["message"]["topic"]
    client_id = request["message"]["from"]
    payload = request["message"]["payload"]
    timestamp = int(request["message"]["timestamp"])
    data_type = None
    try:
        _, _, stream_id = topic.split("/")
        data_type = (
            db.session.query(Stream.data_type).filter(Stream.stream_id == stream_id).scalar()
        )
        if data_type:
            if data_type == "float":
                payload = float(payload)
            if data_type == "int":
                payload = int(payload)
            if data_type == "bool":
                payload = bool(payload)
            if data_type == "char":
                payload = str(payload, encoding="utf-8")
            data = EmqxData(
                node=node,
                msg_id=msg_id,
                client_id=client_id,
                topic=topic,
                stream_id=stream_id,
                payload=str(payload),
                timestamp=datetime.fromtimestamp(timestamp / 1000),
            )
            db.session.add(data)
            db.session.commit()
    except ValueError:
        logger.warning(f"数据格式不正确:  {payload} -> {data_type}")
    except Exception:
        logger.exception("save data field")
