import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name_surname = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    group_facult = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    photoid = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=-1)
    barcode = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    passwordhash = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    login = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    blank_id = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    rights = sqlalchemy.Column(sqlalchemy.Text, nullable=True, default='')