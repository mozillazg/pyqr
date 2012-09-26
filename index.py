#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bae.core.wsgi import WSGIApplication
import main

app = main.app.wsgifunc()
application = WSGIApplication(app)
