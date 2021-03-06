#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Desc    : 
"""

from models.problem import Base as Pbase
from models.doc_mg import Base as doc_base
from models.faq import Base as faq_base
from websdk.consts import const
from settings import settings as app_settings
# ORM创建表结构
from sqlalchemy import create_engine

default_configs = app_settings[const.DB_CONFIG_ITEM][const.DEFAULT_DB_KEY]
engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
    default_configs.get(const.DBUSER_KEY),
    default_configs.get(const.DBPWD_KEY),
    default_configs.get(const.DBHOST_KEY),
    default_configs.get(const.DBPORT_KEY),
    default_configs.get(const.DBNAME_KEY),
), encoding='utf-8', echo=True)


def create():
    # Abase.metadata.create_all(engine)
    Pbase.metadata.create_all(engine)
    doc_base.metadata.create_all(engine)
    faq_base.metadata.create_all(engine)
    print('[Success] 表结构创建成功!')


def drop():
    # Abase.metadata.drop_all(engine)
    Pbase.metadata.drop_all(engine)
    doc_base.metadata.drop_all(engine)


if __name__ == '__main__':
    create()
