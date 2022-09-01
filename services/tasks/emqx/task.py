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
        items = topic.split("/")
        if len(items) != 3 or not items[-1] or client_id != items[1]:
            return
        stream_id = items[-1]
        stream = (
            db.session.query(Stream)
            .filter(
                Stream.stream_id == stream_id,
                Stream.save_data == True,
            )
            .first()
        )
        if stream:
            payload = check_and_convert_payload(payload)
            data = EmqxData(
                node=node,
                msg_id=msg_id,
                client_id=client_id,
                topic=topic,
                stream_id=stream_id,
                payload=payload,
                timestamp=datetime.fromtimestamp(timestamp / 1000),
            )
            db.session.add(data)
            db.session.commit()
    except ValueError:
        logger.warning(f"数据格式不正确: {payload}: {type(payload)} -> {data_type}")
    except Exception:
        logger.exception("save data field")


def check_and_convert_payload(payload: str) -> str:
    if payload.isdigit():
        return payload
    payload = float(payload)
    return str(round(payload, 2))
