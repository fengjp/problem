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


class Docxs(Base):
    __tablename__ = 'pb_docxs'

    ### 上传文档表
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    f_name = Column('f_name', String(50), default='')
    f_size = Column('f_size', String(50), default='')   # 单位 字节/b
    f_url = Column('f_url', String(100), default='')
    sysID = Column('sysID', Integer, default=0)         # 关联的应用系统ID
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)


