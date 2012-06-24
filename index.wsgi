#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# if sys.getdefaultencoding() != 'utf-8':
    # reload(sys)
    # sys.setdefaultencoding('utf-8')

import sae
import web
import main

app = main.app
application = sae.create_wsgi_app(app.wsgifunc())

 
