#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import web

# 将 lib 目录添加到系统路径，以便导入 lib 目录下的模块
app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'lib'))
# 本地化语言文件路径
localedir = app_root + '/i18n'
# 语言文件名称
localefile = 'messages'

# 判断是线上还是本地环境
if 'SERVER_SOFTWARE' in os.environ:
    # SAE
    site = 'http://%s.sinaapp.com' % (os.environ.get('APP_NAME'))
else:
    # Local
    site = 'http://127.0.0.1:8080'
    web.config.debug = True

# urls
url_mode = 'main.'
urls = (
    # 首页
    '/', url_mode + 'Index',
    # 二维码图片
    '/qr', url_mode + 'QR',
)

# 应用模板
# 模板路径
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
# 注册一个全局应用
app = web.application(urls, globals())
# 模板全局变量
web.template.Template.globals['site'] = site
