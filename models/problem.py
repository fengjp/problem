#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
author : shenshuo
date   : 2018年10月23日
desc   : 管理后台数据库
"""

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


class CaseUsers(Base):
    __tablename__ = 'mg_case'

    ### 用户表
    user_id = Column('user_id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(50), unique=True)
    # password = Column('password', String(100))
    # nickname = Column('nickname', String(100))
    # email = Column('email', String(80), unique=True)  ### 邮箱
    tel = Column('tel', String(11))  ### 手机号
    # //wechat = Column('wechat', String(50))  ### 微信号
    no = Column('no', String(50))  ### 工号
    company = Column('company', String(100))  ### 部门
    department = Column('department', String(50))  ### 部门
    # google_key = Column('google_key', String(80))  ### 谷歌认证秘钥
    # superuser = Column('superuser', String(5), default='10')  ### 超级用户  0代表超级用户
    # status = Column('status', String(5), default='0')
    # last_ip = Column('last_ip', String(20), default='')
    # last_login = Column('last_login', DateTime(), default=datetime.now, onupdate=datetime.now)
    ctime = Column('ctime', DateTime(), default=datetime.now)


class CaseList(Base):
    __tablename__ = 'mg_caselist'

    ###问题表
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    case_num = Column('case_num', String(50), unique=True)  # 个案编号
    case_name = Column('case_name', String(50))             # 个案名称
    case_type = Column('case_type', String(10))             # 个案类型
    case_status = Column('case_status', String(10))         # 个案状态
    case_priority = Column('case_priority', String(100))    # 优先级
    case_executor = Column('case_executor', String(100))                  # 处理人
    demander = Column('demander', String(100))            # 联系人
    case_creator = Column('case_creator', String(100))            # 联系人
    case_details = Column('case_details', String(1024))             # 详情描述
    case_source = Column('case_source', String(100))        # 来源
    case_obj = Column('case_obj', String(100))              # 项目
    demand_unit = Column('demand_unit', String(100))        # 需求单位
    case_stime = Column('case_stime', DateTime())             #
    case_etime = Column('case_etime', DateTime(), default=datetime.now)                 #
    case_ltime = Column('case_ltime', String(100))  # 时长
    ctime = Column('ctime', DateTime(), default=datetime.now)  # 记录时间


class CaseUserslist(Base):
    __tablename__ = 'mg_caseuser'

    ### 客户表
    user_id = Column('user_id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(50), unique=True)
    # password = Column('password', String(100))
    # nickname = Column('nickname', String(100))
    # email = Column('email', String(80), unique=True)  ### 邮箱
    tel = Column('tel', String(11))  ### 手机号
    # //wechat = Column('wechat', String(50))  ### 微信号
    company = Column('company', String(100))  ###
    department = Column('department', String(50))  ### 部门
    # google_key = Column('google_key', String(80))  ### 谷歌认证秘钥
    # superuser = Column('superuser', String(5), default='10')  ### 超级用户  0代表超级用户
    # status = Column('status', String(5), default='0')
    # last_ip = Column('last_ip', String(20), default='')
    # last_login = Column('last_login', DateTime(), default=datetime.now, onupdate=datetime.now)
    ctime = Column('ctime', DateTime(), default=datetime.now)

class PlanList(Base):
    __tablename__ = 'mg_planlist'

    ###计划工作表
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    plan_num = Column('plan_num', String(50), unique=True)  # 个案编号
    plan_name = Column('plan_name', String(50))             # 个案名称
    plan_type = Column('plan_type', String(10))             # 个案类型
    plan_status = Column('plan_status', String(10))         # 个案状态
    plan_priority = Column('plan_priority', String(100))    # 优先级
    plan_executor = Column('plan_executor', String(100))                  # 处理人
    demander = Column('demander', String(100))            # 联系人
    plan_creator = Column('plan_creator', String(100))            # 联系人
    plan_details = Column('plan_details', String(1024))             # 详情描述
    plan_source = Column('plan_source', String(100))        # 来源
    plan_obj = Column('plan_obj', String(100))              # 项目
    demand_unit = Column('demand_unit', String(100))        # 需求单位
    plan_stime = Column('plan_stime', DateTime())             #
    plan_etime = Column('plan_etime', DateTime(), default=datetime.now)                 #
    plan_ltime = Column('plan_ltime', String(100))  # 时长
    ctime = Column('ctime', DateTime(), default=datetime.now)  # 记录时间

class TypeList(Base):
    __tablename__ = 'mg_typelist'

    ###计划工作表
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    typename = Column('typename', String(100), unique=True)  # 类型名
    remarks = Column('remarks', String(1024))             # 描述
    chart = Column('chart', String(300))             # 流程图url
    ctime = Column('ctime', DateTime(), default=datetime.now)  # 记录时间