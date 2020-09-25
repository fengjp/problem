#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
Author : shenshuo
date   : 2017-10-11
role   : 管理端 Application
"""

from websdk.application import Application as myApplication
from pb.handlers.penson_handler import penson_urls
from pb.handlers.plan_handler import plan_urls
from pb.handlers.doc_handler import doc_mg_urls
from pb.handlers.faq_handler import faq_urls
from pb.handlers.type_handler import typeList_urls

class Application(myApplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(penson_urls)
        urls.extend(plan_urls)
        urls.extend(doc_mg_urls)
        urls.extend(faq_urls)
        urls.extend(typeList_urls)
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass
