#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sae
import conf

app = conf.app
application = sae.create_wsgi_app(app.wsgifunc())
