from time import time
import sqlalchemy
from .db_session import SqlAlchemyBase


class Event(SqlAlchemyBase):
    __tablename__ = 'logs'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    userid = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=int(time()))
