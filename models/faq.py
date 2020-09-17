#!/usr/bin/env python
# -*-coding:utf-8-*-

from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from datetime import datetime

Base = declarative_base()


def model_to_dict(model):
    model_dict = {}
    for key, column in class_mapper(model.__class__).c.items():
        model_dict[column.name] = getattr(model, key, None)
    return model_dict


class Faq(Base):
    __tablename__ = 'faq'

    ### FAQ
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    question = Column('question', String(100), default='')
    answer = Column('answer', Text, default='')
    clicks = Column('clicks', Integer, default=0)
    sysID = Column('sysID', Integer, default=0)
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)


