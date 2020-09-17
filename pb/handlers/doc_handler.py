#!/usr/bin/env python
# -*-coding:utf-8-*-
import json
import os
import re
from libs.base_handler import BaseHandler
from websdk.db_context import DBContext
from models.doc_mg import Docxs
from websdk.consts import const
from websdk.cache_context import cache_conn
from websdk.web_logs import ins_log
from sqlalchemy import or_, and_
from docx import Document
import urllib
from settings import onlinePreview


def getPreviewUrl(request, file):
    url = urllib.parse.quote_plus('http://' + request.host + '/static/doc/' + file)
    onlinePreviewurl = onlinePreview.format(request.host_name)
    viewUrl = '{0}{1}&officePreviewType=pdf'.format(onlinePreviewurl, url)
    return viewUrl


def readDocx(request, files, keyword=''):
    Base_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    doc_path = '{}/static/doc'.format(Base_DIR)
    doc_list = []
    count = 0
    word = keyword
    if files == 'all':
        _, _, files = os.walk(doc_path).__next__()

    for f in files:
        viewUrl = getPreviewUrl(request, f)
        doc_obj = {
            'title': f,
            'content': '',
            'url': viewUrl
        }
        f_path = os.path.join(doc_path, f)
        file = Document(f_path)
        for para in file.paragraphs:
            if not word:
                doc_obj['content'] = doc_obj['content'] + para.text
            else:
                m = re.search(r'.*{0}.*'.format(word), para.text, re.I)
                if m != None:
                    doc_obj['content'] = doc_obj['content'] + para.text
                    # word = ''

            if len(doc_obj['content']) > 200:
                doc_obj['content'] = doc_obj['content'] + '......'
                break

        if doc_obj['content']:
            doc_list.append(doc_obj)

    count = len(doc_list)
    return doc_list, count


class DocManagerFileHandler(BaseHandler):
    def get(self):
        page = int(self.get_argument('page', 1))  # 开始页
        limit = int(self.get_argument('limit', 10))  # 要查询条数
        keyword = self.get_argument('value', '')  # 关键字搜索
        tag_json = self.get_argument('key', '')  # 分类
        try:
            tags = json.loads(tag_json)
        except:
            tags = ['0']
        files = []
        if len(tags) > 0:
            if '0' in tags:
                files = 'all'

            else:
                with DBContext('r') as session:
                    res_f = session.query(Docxs.f_name).filter(Docxs.sysID.in_(tags)).all()
                    files = [i.f_name for i in res_f]
        # ins_log.read_log('info', files)
        # ins_log.read_log('info', tags)
        limit_start = (page - 1) * limit
        doc_list, count = readDocx(self.request, files, keyword)
        doc_list = doc_list[limit_start:limit * page]
        return self.write(dict(code=0, msg="获取成功", count=count, data=doc_list))

    def post(self):
        data = json.loads(self.request.body.decode("utf-8"))
        sysID = data.get('sysID')
        uploadList = data.get('uploadList')
        for file in uploadList:
            f_size = file['size']  # 单位 字节/b
            f_name = file['name']
            f_url = file['url']

            if not f_name:
                return self.write(dict(code=-1, msg='文档名称不能为空'))

            with DBContext('r') as session:
                exist_id = session.query(Docxs.id).filter(Docxs.f_name == f_name).first()

            if exist_id:
                with DBContext('w', None, True) as session:
                    session.query(Docxs).filter(Docxs.f_name == f_name).update({
                        Docxs.f_name: f_name,
                        Docxs.f_size: f_size,
                        Docxs.f_url: f_url,
                        Docxs.sysID: sysID,
                    }, synchronize_session=False)

            else:
                with DBContext('w', None, True) as session:
                    new_docx = Docxs(
                        f_name=f_name,
                        f_size=f_size,
                        f_url=f_url,
                        sysID=sysID,
                    )
                    session.add(new_docx)

        return self.write(dict(code=0, msg='保存成功'))


class UpLoadFileHandler(BaseHandler):
    def post(self, *args, **kwargs):
        ###文件保存到本地
        Base_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        upload_path = '{}/static/doc'.format(Base_DIR)
        file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据
        ret = {'result': 'OK', 'msg': "上传成功", 'code': 0}
        if not file_metas:
            ret['result'] = 'Invalid Args'
            ret['msg'] = '上传失败'
            ret['code'] = 1
            ret['url'] = ''
            return ret

        for meta in file_metas:
            filename = meta['filename']
            # print('filename---->', filename)
            ret['url'] = 'http://' + self.request.host + '/static/doc/' + filename
            file_path = os.path.join(upload_path, filename)
            with open(file_path, 'wb') as up:
                up.write(meta['body'])

        self.write(json.dumps(ret))


doc_mg_urls = [
    (r"/v1/pb/doc/upload/", UpLoadFileHandler),
    (r"/v1/pb/doc/", DocManagerFileHandler),
]

if __name__ == "__main__":
    print(readDocx({}, 'all'))
    pass
