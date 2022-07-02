# coding: utf-8
from sqlalchemy import (
    Text,
    Float,
    Index,
    Column,
    String,
    Boolean,
    Integer,
    DateTime,
    ForeignKey,
    SmallInteger,
    CheckConstraint,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import INET, JSONB

Base = declarative_base()
metadata = Base.metadata


class Chart(Base):
    __tablename__ = "chart"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('device_chart_id_seq'::regclass)")
    )
    chart_id = Column(String(22), nullable=False, unique=True)
    title = Column(String(16))
    created_time = Column(DateTime(True), nullable=False)
    create_user_id = Column(Integer, nullable=False, index=True)
    device_id = Column(Integer, index=True)
    custom_settings = Column(JSONB(astext_type=Text()))
    update_time = Column(DateTime(True), nullable=False)
    name = Column(String(16), nullable=False)
    sequence = Column(Integer, nullable=False)
    last_update_user_id = Column(Integer, index=True)


class ChartStream(Base):
    __tablename__ = "chart_streams"
    __table_args__ = (UniqueConstraint("chart_id", "stream_id"),)

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('device_chart_streams_id_seq'::regclass)"),
    )
    chart_id = Column(Integer, nullable=False, index=True)
    stream_id = Column(Integer, nullable=False, index=True)


class Device(Base):
    __tablename__ = "device"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('device_id_seq'::regclass)")
    )
    created_time = Column(DateTime(True), nullable=False)
    update_time = Column(DateTime(True), nullable=False)
    client_id = Column(String(12), nullable=False, unique=True)
    client_name = Column(String(12), nullable=False, unique=True)
    name = Column(String(8), nullable=False)
    desc = Column(Text)
    status = Column(Boolean, nullable=False)
    image = Column(String(100))
    is_super = Column(Boolean, nullable=False)
    sequence = Column(Integer, nullable=False)
    last_connect_time = Column(DateTime(True))
    token = Column(String(16), nullable=False)
    category_id = Column(Integer, index=True)
    create_user_id = Column(Integer, nullable=False, index=True)
    last_update_user_id = Column(Integer, index=True)
    custom_info = Column(String(64))


class DeviceCategory(Base):
    __tablename__ = "device_category"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('device_category_id_seq'::regclass)"),
    )
    created_time = Column(DateTime(True), nullable=False)
    update_time = Column(DateTime(True), nullable=False)
    name = Column(String(8), nullable=False)
    sequence = Column(Integer, nullable=False)
    create_user_id = Column(Integer, nullable=False, index=True)
    last_update_user_id = Column(Integer, index=True)


class EmqxAcl(Base):
    __tablename__ = "emqx_acl"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('mqtt_acl_id_seq'::regclass)")
    )
    allow = Column(Integer, nullable=False)
    ipaddr = Column(String(60), nullable=False)
    username = Column(String(100), nullable=False)
    clientid = Column(String(100), nullable=False)
    access = Column(Integer, nullable=False)
    topic = Column(String(100), nullable=False)


class EmqxData(Base):
    __tablename__ = "emqx_data"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('emqx_data_id_seq'::regclass)")
    )
    node = Column(String(32), nullable=False)
    msg_id = Column(String(64), nullable=False)
    client_id = Column(String(64), nullable=False, index=True)
    topic = Column(String(128), nullable=False, index=True)
    payload = Column(String(256), nullable=False)
    timestamp = Column(DateTime(True), nullable=False)


class EmqxLog(Base):
    __tablename__ = "emqx_log"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('emqx_logs_id_seq'::regclass)")
    )
    node = Column(String(32), nullable=False)
    ip = Column(INET, nullable=False)
    port = Column(String(8), nullable=False)
    client_id = Column(String(32), nullable=False)
    proto = Column(String(32), nullable=False)
    connected = Column(Boolean, nullable=False)


class Stream(Base):
    __tablename__ = "stream"
    __table_args__ = (UniqueConstraint("device_id", "name"),)

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('stream_id_seq'::regclass)")
    )
    created_time = Column(DateTime(True), nullable=False)
    update_time = Column(DateTime(True), nullable=False)
    stream_id = Column(String(22), nullable=False, unique=True)
    name = Column(String(16), nullable=False)
    unit_name = Column(String(8), nullable=False)
    unit = Column(String(8), nullable=False)
    qos = Column(Integer, nullable=False)
    data_type = Column(String(8), nullable=False)
    create_user_id = Column(Integer, nullable=False, index=True)
    device_id = Column(Integer, nullable=False, index=True)
    last_update_user_id = Column(Integer, index=True)
    icon = Column(String(32))
    image = Column(String(100))
    show = Column(Boolean, nullable=False)


class Trigger(Base):
    __tablename__ = "trigger"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('device_trigger_id_seq'::regclass)")
    )
    trigger_id = Column(String(22), nullable=False, unique=True)
    url = Column(String(200), nullable=False)
    condition = Column(String(8), nullable=False)
    threshold_value = Column(Float(53), nullable=False)
    trigger_type = Column(String(12), nullable=False)
    start_time = Column(DateTime(True))
    end_time = Column(DateTime(True))
    active = Column(Boolean, nullable=False)
    created_time = Column(DateTime(True), nullable=False)
    create_user_id = Column(Integer, nullable=False, index=True)
    device_id = Column(Integer, nullable=False, index=True)
    stream_id = Column(Integer, nullable=False, index=True)
    update_time = Column(DateTime(True), nullable=False)
    last_update_user_id = Column(Integer, index=True)


class TriggerLog(Base):
    __tablename__ = "trigger_log"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('device_triggerlog_id_seq'::regclass)"),
    )
    result = Column(Text, nullable=False)
    success = Column(Boolean, nullable=False)
    value = Column(String(32), nullable=False)
    create_date = Column(DateTime(True), nullable=False)
    device_id = Column(
        ForeignKey("device.id", deferrable=True, initially="DEFERRED"), nullable=False, index=True
    )
    stream_id = Column(
        ForeignKey("stream.id", deferrable=True, initially="DEFERRED"), nullable=False, index=True
    )
    trigger_id = Column(ForeignKey("trigger.id", deferrable=True, initially="DEFERRED"), index=True)

    device = relationship("Device")
    stream = relationship("Stream")
    trigger = relationship("Trigger")
