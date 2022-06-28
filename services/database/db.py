from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DB(object):
    def __init__(self):
        engine = create_engine("postgresql+psycopg2://admin:admin@127.0.0.1/link")
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def reconnect(self):
        """ "断开重连"""
        self.session = self.Session()


db = DB()
