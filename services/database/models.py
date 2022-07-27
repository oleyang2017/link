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


class AuthGroup(Base):
    __tablename__ = "auth_group"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('auth_group_id_seq'::regclass)")
    )
    name = Column(String(150), nullable=False, unique=True)


class AuthUser(Base):
    __tablename__ = "auth_user"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('auth_user_id_seq'::regclass)")
    )
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime(True))
    is_superuser = Column(Boolean, nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime(True), nullable=False)
    username = Column(String(128), nullable=False, unique=True)
    mobile = Column(String(20), unique=True)
    wx_open_id = Column(String(64), nullable=False, index=True)
    wx_union_id = Column(String(64), nullable=False, index=True)
    gender = Column(String(1), nullable=False)
    desc = Column(Text, nullable=False)
    avatar = Column(String(100))
    avatar_url = Column(String(200))
    address = Column(String(128), nullable=False)
    access_token = Column(String(24), nullable=False, unique=True)
    created_time = Column(DateTime(True), nullable=False)


class Chart(Base):
    __tablename__ = "chart"

    id = Column(Integer, primary_key=True, server_default=text("nextval('chart_id_seq'::regclass)"))
    created_time = Column(DateTime(True), nullable=False)
    update_time = Column(DateTime(True), nullable=False)
    chart_id = Column(String(22), nullable=False, unique=True)
    title = Column(String(16))
    name = Column(String(16), nullable=False)
    custom_settings = Column(JSONB(astext_type=Text()))
    sequence = Column(Integer, nullable=False)
    create_user_id = Column(Integer, nullable=False, index=True)
    device_id = Column(Integer, index=True)
    last_update_user_id = Column(Integer, index=True)


class ChartStream(Base):
    __tablename__ = "chart_streams"
    __table_args__ = (UniqueConstraint("chart_id", "stream_id"),)

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('chart_streams_id_seq'::regclass)")
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
    name = Column(String(8), nullable=False)
    desc = Column(Text)
    status = Column(Boolean, nullable=False)
    image = Column(String(100))
    is_super = Column(Boolean, nullable=False)
    sequence = Column(Integer, nullable=False)
    last_connect_time = Column(DateTime(True))
    custom_info = Column(String(64))
    category_id = Column(Integer, index=True)
    create_user_id = Column(Integer, nullable=False, index=True)
    last_update_user_id = Column(Integer, index=True)
    image_url = Column(String(256))


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


class DjangoContentType(Base):
    __tablename__ = "django_content_type"
    __table_args__ = (UniqueConstraint("app_label", "model"),)

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('django_content_type_id_seq'::regclass)"),
    )
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class DjangoMigration(Base):
    __tablename__ = "django_migrations"

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('django_migrations_id_seq'::regclass)"),
    )
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DateTime(True), nullable=False)


class DjangoSession(Base):
    __tablename__ = "django_session"

    session_key = Column(String(40), primary_key=True, index=True)
    session_data = Column(Text, nullable=False)
    expire_date = Column(DateTime(True), nullable=False, index=True)


class EmqxAcl(Base):
    __tablename__ = "emqx_acl"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('emqx_acl_id_seq'::regclass)")
    )
    allow = Column(Integer, nullable=False)
    ipaddr = Column(String(60), nullable=False)
    username = Column(String(100), nullable=False)
    clientid = Column(String(100), nullable=False)
    access = Column(Integer, nullable=False)
    topic = Column(String(100), nullable=False)


class EmqxDatum(Base):
    __tablename__ = "emqx_data"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('emqx_data_id_seq'::regclass)")
    )
    node = Column(String(32), nullable=False)
    msg_id = Column(String(64), nullable=False)
    client_id = Column(String(64), nullable=False, index=True)
    stream_id = Column(String(64), nullable=False, index=True)
    topic = Column(String(128), nullable=False)
    payload = Column(String(256), nullable=False)
    timestamp = Column(DateTime(True), nullable=False)


class EmqxLog(Base):
    __tablename__ = "emqx_log"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('emqx_log_id_seq'::regclass)")
    )
    node = Column(String(32), nullable=False)
    ip = Column(INET, nullable=False)
    port = Column(String(8), nullable=False)
    client_id = Column(String(32), nullable=False)
    proto = Column(String(32), nullable=False)
    connected = Column(Boolean, nullable=False)


class EmqxUser(Base):
    __tablename__ = "emqx_user"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('emqx_user_id_seq'::regclass)")
    )
    username = Column(String(12), nullable=False, unique=True)
    password = Column(String(12), nullable=False)
    user_id = Column(Integer, nullable=False, index=True)


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
    show = Column(Boolean, nullable=False)
    image = Column(String(100))
    icon = Column(String(32))
    color = Column(String(32))
    create_user_id = Column(Integer, nullable=False, index=True)
    device_id = Column(Integer, nullable=False, index=True)
    last_update_user_id = Column(Integer, index=True)


class Trigger(Base):
    __tablename__ = "trigger"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('trigger_id_seq'::regclass)")
    )
    created_time = Column(DateTime(True), nullable=False)
    update_time = Column(DateTime(True), nullable=False)
    trigger_id = Column(String(22), nullable=False, unique=True)
    url = Column(String(200), nullable=False)
    condition = Column(String(8), nullable=False)
    threshold_value = Column(Float(53), nullable=False)
    trigger_type = Column(String(12), nullable=False)
    start_time = Column(DateTime(True))
    end_time = Column(DateTime(True))
    active = Column(Boolean, nullable=False)
    create_user_id = Column(Integer, nullable=False, index=True)
    device_id = Column(Integer, nullable=False, index=True)
    last_update_user_id = Column(Integer, index=True)
    stream_id = Column(Integer, nullable=False, index=True)


class AuthPermission(Base):
    __tablename__ = "auth_permission"
    __table_args__ = (UniqueConstraint("content_type_id", "codename"),)

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('auth_permission_id_seq'::regclass)"),
    )
    name = Column(String(255), nullable=False)
    content_type_id = Column(
        ForeignKey("django_content_type.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    codename = Column(String(100), nullable=False)

    content_type = relationship("DjangoContentType")


class AuthUserGroup(Base):
    __tablename__ = "auth_user_groups"
    __table_args__ = (UniqueConstraint("userprofile_id", "group_id"),)

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('auth_user_groups_id_seq'::regclass)"),
    )
    userprofile_id = Column(
        ForeignKey("auth_user.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    group_id = Column(
        ForeignKey("auth_group.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )

    group = relationship("AuthGroup")
    userprofile = relationship("AuthUser")


class DjangoAdminLog(Base):
    __tablename__ = "django_admin_log"
    __table_args__ = (CheckConstraint("action_flag >= 0"),)

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('django_admin_log_id_seq'::regclass)"),
    )
    action_time = Column(DateTime(True), nullable=False)
    object_id = Column(Text)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(SmallInteger, nullable=False)
    change_message = Column(Text, nullable=False)
    content_type_id = Column(
        ForeignKey("django_content_type.id", deferrable=True, initially="DEFERRED"), index=True
    )
    user_id = Column(
        ForeignKey("auth_user.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )

    content_type = relationship("DjangoContentType")
    user = relationship("AuthUser")


class TriggerLog(Base):
    __tablename__ = "trigger_log"

    id = Column(
        Integer, primary_key=True, server_default=text("nextval('trigger_log_id_seq'::regclass)")
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


class AuthGroupPermission(Base):
    __tablename__ = "auth_group_permissions"
    __table_args__ = (UniqueConstraint("group_id", "permission_id"),)

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('auth_group_permissions_id_seq'::regclass)"),
    )
    group_id = Column(
        ForeignKey("auth_group.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    permission_id = Column(
        ForeignKey("auth_permission.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )

    group = relationship("AuthGroup")
    permission = relationship("AuthPermission")


class AuthUserUserPermission(Base):
    __tablename__ = "auth_user_user_permissions"
    __table_args__ = (UniqueConstraint("userprofile_id", "permission_id"),)

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('auth_user_user_permissions_id_seq'::regclass)"),
    )
    userprofile_id = Column(
        ForeignKey("auth_user.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    permission_id = Column(
        ForeignKey("auth_permission.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )

    permission = relationship("AuthPermission")
    userprofile = relationship("AuthUser")


class GuardianGroupobjectpermission(Base):
    __tablename__ = "guardian_groupobjectpermission"
    __table_args__ = (
        UniqueConstraint("group_id", "permission_id", "object_pk"),
        Index("guardian_gr_content_ae6aec_idx", "content_type_id", "object_pk"),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('guardian_groupobjectpermission_id_seq'::regclass)"),
    )
    object_pk = Column(String(255), nullable=False)
    content_type_id = Column(
        ForeignKey("django_content_type.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    group_id = Column(
        ForeignKey("auth_group.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    permission_id = Column(
        ForeignKey("auth_permission.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )

    content_type = relationship("DjangoContentType")
    group = relationship("AuthGroup")
    permission = relationship("AuthPermission")


class GuardianUserobjectpermission(Base):
    __tablename__ = "guardian_userobjectpermission"
    __table_args__ = (
        UniqueConstraint("user_id", "permission_id", "object_pk"),
        Index("guardian_us_content_179ed2_idx", "content_type_id", "object_pk"),
    )

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('guardian_userobjectpermission_id_seq'::regclass)"),
    )
    object_pk = Column(String(255), nullable=False)
    content_type_id = Column(
        ForeignKey("django_content_type.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    permission_id = Column(
        ForeignKey("auth_permission.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        ForeignKey("auth_user.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )

    content_type = relationship("DjangoContentType")
    permission = relationship("AuthPermission")
    user = relationship("AuthUser")
