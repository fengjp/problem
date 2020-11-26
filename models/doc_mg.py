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
    f_size = Column('f_size', String(50), default='')  # 单位 字节/b
    f_url = Column('f_url', String(100), default='')
    sysID = Column('sysID', Integer, default=0)  # 关联的应用系统ID
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)


class FoldersDir(Base):
    __tablename__ = 'folders_dir'

    ### 文件目录
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    folderName = Column('folderName', String(50), default='')  # 文件夹名称
    authority = Column('authority', String(50), default='')  # 权限
    ftype = Column('ftype', Integer, default=0)  # 文件夹类型 0 私密 1 公共
    nickName = Column('nickName', String(50), default='')  # 创建人昵称
    userID = Column('userID', Integer, default=0)  # 创建人ID
    preID = Column('preID', Integer, default=0)  # 上级目录ID
    ctime = Column('ctime', DateTime(), default=datetime.now, onupdate=datetime.now)
