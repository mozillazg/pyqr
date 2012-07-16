#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# if sys.getdefaultencoding() != 'utf-8':
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
import os

app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'lib'))

import sae
import web
import main

app = main.app
application = sae.create_wsgi_app(app.wsgifunc())

