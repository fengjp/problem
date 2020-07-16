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

class Application(myApplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(penson_urls)
        urls.extend(plan_urls)
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass
