from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DB(object):
    def __init__(self):
        engine = create_engine("postgresql+psycopg2://admin:admin@link_pgsql/link")
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def reconnect(self):
        """ "断开重连"""
        logger.info("reconnect database")
        self.session = self.Session()


db = DB()
