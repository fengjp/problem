#!/usr/bin/env python
# -*-coding:utf-8-*-


import json
import shortuuid
import base64
from websdk.jwt_token import gen_md5
from websdk.tools import check_password
from libs.base_handler import BaseHandler
from websdk.db_context import DBContext
from models.problem import TypeList, model_to_dict
from websdk.consts import const
from websdk.cache_context import cache_conn
from websdk.tools import convert
from websdk.web_logs import ins_log
import os
import pandas as pd


class TypeListHandler(BaseHandler):
    def get(self, *args, **kwargs):
        data_list = []
        key = self.get_argument('key', default=None, strip=True)
        value = self.get_argument('value', default=None, strip=True)
        page_size = self.get_argument('page', default=1, strip=True)
        limit = self.get_argument('limit', default=30, strip=True)
        limit_start = (int(page_size) - 1) * int(limit)
        user_list = []
        with DBContext('r') as session:
            conditions = []
            if key == "typename":
                conditions.append(TypeList.typename.like('%{}%'.format(value)))
            if key == "remarks":
                conditions.append(TypeList.remarks.like('%{}%'.format(value)))
            if key == "chart":
                conditions.append(TypeList.chart.like('%{}%'.format(value)))

            todata = session.query(TypeList).filter(*conditions).order_by(TypeList.ctime.desc()).offset(
                limit_start).limit(int(limit)).all()
            tocount = session.query(TypeList).filter(*conditions).count()

        for msg in todata:
            case_dict = {}
            data_dict = model_to_dict(msg)
            case_dict["id"] = data_dict["id"]
            case_dict["typename"] = data_dict["typename"]
            case_dict["remarks"] = data_dict["remarks"]
            case_dict["chart"] = data_dict["chart"]
            case_dict["ctime"] = str(data_dict["ctime"])
            data_list.append(case_dict)

        if len(data_list) > 0:
             return  self.write(dict(code=0, msg='获取成功', count=tocount, data=data_list))
        else:
             return  self.write(dict(code=-1, msg='没有相关数据', count=0, data=[]))

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        typename = str(data.get('typename', None)).replace(" ", "") #去除数据中的空格
        remarks = data.get('remarks', None)
        chart = data.get('chart', None)

        with DBContext('r') as session:
            typename_str = session.query(TypeList).filter(TypeList.typename  ==  typename).first()
        if typename_str :
            return self.write(dict(code=-1, msg="类型名已存在。"))
        with DBContext('w', None, True) as session:
            session.add(TypeList(
                typename=typename,
                remarks=remarks,
                chart=chart,

            ))
            session.commit()

        return  self.write(dict(code=0, msg='成功', count=0, data=[]))

    def delete(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        id = data.get('id', None)
        if not id:
            return self.write(dict(code=-1, msg='ID不能为空'))

        with DBContext('w', None, True) as session:
            session.query(TypeList).filter(TypeList.id == id).delete(synchronize_session=False)
        return   self.write(dict(code=0, msg='删除成功'))

    def put(self, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))
        id = data.get('id', None)
        typename = data.get('typename', None)
        remarks = data.get('remarks', None)
        chart = data.get('chart', None)

        try:
            with DBContext('w', None, True) as session:
                session.query(TypeList).filter(TypeList.id == id).update({
                    TypeList.typename: typename,
                    TypeList.remarks: remarks,
                    TypeList.chart: chart,
                })
                session.commit()
        except Exception as e:
            return self.write(dict(code=-2, msg='修改失败，请检查数据是否合法或者重复'))
        return self.write(dict(code=0, msg='编辑成功'))

class uploadtypeList(BaseHandler):
    def post(self, *args, **kwargs):
        ###文件保存到本地
        data_list = {}
        Base_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        upload_path = '{}/static/report/files/imges/'.format(Base_DIR)
        file_name = self.request.files["file"][0]["filename"] #图片文件名
        file_body = self.request.files["file"][0]["body"]     #图片文件内容
        # ins_log.read_log('info', "800000000000000000000000000000000000")
        # ins_log.read_log('info', self.request.files["file"][0]["filename"])
        # ins_log.read_log('info', "800000000000000000000000000000000000")
        file_path = upload_path + "type_" + file_name
        with open(file_path, 'wb') as up:
            up.write(file_body)
        urlstr = "http://" + self.request.host + "/static/report/files/imges/" + "type_" + file_name
        data_list["url"] = urlstr
        return   self.write(dict(code=0, msg='成功',  data=data_list))


class DataHandler(BaseHandler):
    def get(self, *args, **kwargs):
        data_list = []
        value = self.get_argument('value', default=None, strip=True)
        with DBContext('r') as session:
            todata = session.query(TypeList).filter(TypeList.typename == value ).order_by(TypeList.ctime.desc()).all()

        for msg in todata:
            case_dict = {}
            data_dict = model_to_dict(msg)
            case_dict["id"] = data_dict["id"]
            case_dict["typename"] = data_dict["typename"]
            case_dict["remarks"] = data_dict["remarks"]
            case_dict["chart"] = data_dict["chart"]
            case_dict["ctime"] = str(data_dict["ctime"])
            data_list.append(case_dict)

        if len(data_list) > 0:
             return  self.write(dict(code=0, msg='获取成功',  data=data_list))
        else:
             return  self.write(dict(code=-1, msg='没有相关数据', count=0, data=[]))


typeList_urls = [
    (r"/v2/accounts/typeList/", TypeListHandler),
    (r"/v2/accounts/typedata/", DataHandler),
    (r"/v2/accounts/typeList/upload/", uploadtypeList),
]

if __name__ == "__main__":
    pass
