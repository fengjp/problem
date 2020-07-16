#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
role   : 管理端 Application
"""

from websdk.application import Application as myApplication
from pb.handlers.penson_handler import penson_urls
from pb.handlers.doc_handler import doc_mg_urls

class Application(myApplication):
    def __init__(self, **settings):
        urls = []
        urls.extend(penson_urls)
        urls.extend(doc_mg_urls)
        super(Application, self).__init__(urls, **settings)


if __name__ == '__main__':
    pass
