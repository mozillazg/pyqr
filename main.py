#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import StringIO
import web
import qrcode
from mime import ImageMIME

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

web.config.debug = False

urls = (
    '/', 'Index',
    '/qr', 'QR',
)

if 'SERVER_SOFTWARE' in os.environ:
    # SAE
    site = 'http://%s.sinaapp.com' % (os.environ.get('APP_NAME'))
else:
    # Local
    site = 'http://127.0.0.1:8080'

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
app = web.application(urls, globals())
web.template.Template.globals['site'] = site


class Index(object):
    def GET(self):
        api_url = site + '/qr?chs=300x300&chl=http://zh.wikipedia.org/wiki/QR%E7%A2%BC'
        return render.index(api_url)

class QR(object):
    """处理传来的数据并显示 QR Code 二维码图片
    """
    def GET(self):
        # TODO 解决 IE 浏览器下地址栏输入中文出现编码错误的文
        # TODO google 是直接将在地址栏输入的参数重定向为 '' , 不用那么复杂
        # query = web.ctx.query # 它将字符都变成了类似 u'%B3%B5' 导致不能猜测编码 
        query = web.ctx.env['QUERY_STRING'] # 解决非 IE 浏览器下地址栏输入中文出现的编码问题
        print query
        if query == '':
            chl = ''
            chs = '300x300'
        else:
            query = query.split('&')
            query = dict([tuple(i) for i in [x.split('=') for x in query]])
            print query
            # query = web.storage(query)
            # try:
            # text = web.input(chl='', chs='320x320')
            # except UnicodeDecodeError:
                # return web.seeother('/')
            chl = query.get('chl', '')
            chs = query.get('chs', '300x300')
            chl = chl.replace('+', '%20') # 解决空格变加号，替换空格为 '%20'
        print repr(chl)
        import urllib2
        chl = urllib2.unquote(chl)
        print repr(chl)
        import chardet
        dete = chardet.detect(chl)
        print dete
        if dete['confidence'] < 0.99:
            import chardete
            print repr(chl)
            chl = chardete.dete(chl)
            print repr(chl)
            # if charest is None:
                # raise web.seeother('/')
        else:
            charest = dete['encoding']
            chl = chl.decode(charest).encode('utf8')
            print repr(chl)
        if len(chl) > 700:
            # return web.seeother('/')
            chl = ''
        im = qrcode.make(chl)
        try:
            size = tuple([int(i) for i in chs.split('x')])
        except:
            return web.seeother('/')
        # Try to import PIL in either of the two ways it can be installed.
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            import Image, ImageDraw
        # im.show()
        img_name = StringIO.StringIO()
        im.save(img_name, 'png')
        img_data = img_name.getvalue()
        im = Image.open(StringIO.StringIO(img_data))
        # im.show()
        x, y = im.size
        # print im.size
        # print size
        rx, ry = size
        # TODO 缩放太小不能识别则显示空白，判断图片清晰度
        if rx <= ry and rx <= x:
            x = y = rx
        elif ry <= rx and ry <= y:
            x = y = ry
        # 缩放二维码图片
        im = im.resize((x, y), Image.ANTIALIAS)
        new_im = Image.new("1", (rx, ry), "white")
        new_im.paste(im, ((rx-x)/2, (ry-y)/2, rx-(rx-x)/2, ry-(ry-y)/2))
        img_name.close()
        new_im_name = StringIO.StringIO()
        new_im.save(new_im_name, 'png')
        new_im_data = new_im_name.getvalue()
        MIME = ImageMIME().get_image_type(new_im_data)
        new_im_name.close()
        web.header('Content-Type', MIME)
        return new_im_data

if __name__ == '__main__':
    app.run()

