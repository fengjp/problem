#!/usr/bin/env python
# -*-coding:utf-8-*-
import json
import os
import re
from libs.base_handler import BaseHandler
from websdk.db_context import DBContext
from models.faq import Faq, model_to_dict
from websdk.consts import const
from websdk.cache_context import cache_conn
from websdk.web_logs import ins_log
from sqlalchemy import or_, and_
import urllib
from settings import onlinePreview


class DocManagerFileHandler(BaseHandler):
    def get(self):
        page = int(self.get_argument('page', 1))  # 开始页
        tolimit = int(self.get_argument('limit', 10))  # 要查询条数
        keyword = self.get_argument('value', '')  # 关键字搜索
        tag_json = self.get_argument('key', '')  # 分类
        limit_start = (page - 1) * tolimit
        count = 0
        faq_list = []
        res_faq = []
        try:
            tags = json.loads(tag_json)
        except:
            tags = ['0']

        if len(tags) > 0:
            with DBContext('r') as session:
                if '0' in tags:
                    if keyword:
                        conditions = []
                        conditions.append(or_(
                            Faq.question.like('%{}%'.format(keyword)),
                            Faq.answer.like('%{}%'.format(keyword))
                        ))
                        # conditions.append(Faq.answer.like('%{}%'.format(keyword)))
                        res_faq = session.query(Faq).filter(*conditions).order_by(Faq.clicks.desc()).all()
                        count = session.query(Faq).filter(*conditions).count()
                    else:
                        count = session.query(Faq).count()
                        res_faq = session.query(Faq).order_by(Faq.clicks.desc()).all()
                else:
                    if keyword:
                        conditions = []
                        conditions.append(or_(
                            Faq.question.like('%{}%'.format(keyword)),
                            Faq.answer.like('%{}%'.format(keyword))
                        ))
                        conditions.append(Faq.sysID.in_(tags))
                        res_faq = session.query(Faq).filter(*conditions).order_by(Faq.clicks.desc()).all()
                        count = session.query(Faq).filter(*conditions).count()
                    else:
                        count = session.query(Faq).filter(Faq.sysID.in_(tags)).count()
                        res_faq = session.query(Faq).filter(Faq.sysID.in_(tags)).order_by(Faq.clicks.desc()).offset(
                            limit_start).limit(int(tolimit)).all()

        # ins_log.read_log('info', tags)
        # ins_log.read_log('info', res_faq)

        for msg in res_faq:
            data_dict = model_to_dict(msg)
            data_dict['ctime'] = str(data_dict['ctime']).split(' ')[0]
            faq_list.append(data_dict)

        return self.write(dict(code=0, msg="获取成功", count=count, data=faq_list))

    def post(self):
        data = json.loads(self.request.body.decode("utf-8"))
        sysID = data.get('sysID')
        question = data.get('question')
        answer = data.get('answer')
        # ins_log.read_log('info', data)

        if not question:
            return self.write(dict(code=-1, msg='问题不能为空'))

        with DBContext('r') as session:
            exist_id = session.query(Faq.id).filter(Faq.question == question).first()

        if exist_id:
            with DBContext('w', None, True) as session:
                session.query(Faq).filter(Faq.question == question).update({
                    Faq.question: question,
                    Faq.answer: answer,
                    Faq.sysID: sysID,
                }, synchronize_session=False)

        else:
            with DBContext('w', None, True) as session:
                new_faq = Faq(
                    question=question,
                    answer=answer,
                    sysID=sysID,
                )
                session.add(new_faq)

        return self.write(dict(code=0, msg='保存成功'))


faq_urls = [
    (r"/v1/pb/faq/", DocManagerFileHandler),
]

if __name__ == "__main__":
    pass
