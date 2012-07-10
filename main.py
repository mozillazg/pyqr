#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import StringIO
import string
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
    site = 'http://127.0.0.1:8080' # TODO 获取自定义的端口

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)
app = web.application(urls, globals())
web.template.Template.globals['site'] = site


class Index(object):
    def GET(self):
        return render.index()

class QR(object):
    """处理传来的数据并显示 QR Code 二维码图片
    """
    def show_image(self, chl, chld, chs):
        """返回图片 MIME 及 内容，用于显示图片
        """
        # Try to import PIL in either of the two ways it can be installed.
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            import Image, ImageDraw
        if len(chl) > 700: # 限制字符数
            chl = ''
        chld = string.upper(chld) # 转换为大小字母
        if chld == '':
            chld = 'L|4'
        chld = chld.split('|') # chld 是非必需参数
        if len(chld) == 2:
            try:
                self.version = int(chld[1])
            except:
                # raise web.badrequest()
                self.version = 4
        elif len(chld) == 1:
            self.version = 4
        if (chld[0] not in ['L', 'M', 'Q', 'H']) or self.version < 1 or self.version > 40:
            # raise web.badrequest()
            chld[0] = 'L'
            self.version = 4
        try:
            chs = string.lower(chs) # 转换为小写字母
            size = tuple([int(i) for i in chs.split('x')])
        except:
            raise web.badrequest()
        else:
            if (size[0] * size[1] == 0 or size[0] < 0 or size[1] < 0 or (
                    size[0] < 21) or size[0] < 21) or (# 处理负数，零，小于最小值（21x21）的情况
                    (size[0] > 500) or size[1] > 500): # 限制图片大小，防止图片太大导致系统死机
                raise web.badrequest()
        if chld[0] == 'L':
            self.error_correction = qrcode.constants.ERROR_CORRECT_L
        elif chld[0] == 'M':
            self.error_correction = qrcode.constants.ERROR_CORRECT_M
        elif chld[0] == 'Q':
            self.error_correction = qrcode.constants.ERROR_CORRECT_Q
        elif chld[0] == 'H':
            self.error_correction = qrcode.constants.ERROR_CORRECT_H
        # self.version = 4
        self.border = 4
        self.size = size[0] if size[0] <= size[1] else size[1]
        # 根据 qrcode 源码及 size 参数求 box_size
        self.box_size = self.size/((self.version * 4 + 17) + self.border * 2)
        qr = qrcode.QRCode(
                version=self.version,
                error_correction=self.error_correction,
                box_size=self.box_size,
                border=self.border,
            )
        qr.add_data(chl)
        qr.make(fit=True)
        im = qr.make_image()
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
        new_im = Image.new("1", (rx, ry), "white")
        paste_size = ((rx-x)/2.00, (ry-y)/2.00, rx-(rx-x)/2.00, ry-(ry-y)/2.00)
        # print paste_size
        new_im.paste(im, paste_size)
        img_name.close()
        new_im_name = StringIO.StringIO()
        new_im.save(new_im_name, 'png')
        new_im_data = new_im_name.getvalue()
        MIME = ImageMIME().get_image_type(new_im_data)
        new_im_name.close()
        return (MIME, new_im_data)

    def GET(self):
        # TODO 解决 IE 浏览器下地址栏输入中文出现编码错误的情况
        # TODO google 是直接将在地址栏输入的参数重定向为 '' , 不用那么复杂
        # query = web.ctx.query # 它及 web.input() 将字符都变成了类似 u'%B3%B5' 导致不能猜测编码 
        query = web.ctx.env['QUERY_STRING'] # 解决非 IE 浏览器下地址栏输入中文出现的编码问题
        # print query
        if query == '':
            return web.badrequest()
        else:
            query = query.split('&')
            try:
                # query = dict([tuple(i) for i in ])
                values = [x.split('=') for x in query] # 分割参数
                query = {}
                for i in values:
                    if len(i) == 1 and i[0] == 'chld': # chld 是非必需参数
                        query.setdefault(i[0], 'L|4')
                    elif len(i) == 2 and i[0] in ['chl', 'chs', 'chld']:
                        query.setdefault(i[0], i[1])
                # print query
            except:
                return web.badrequest()
            chl = query.get('chl', '')
            chl = chl.replace('+', '%20') # 解决空格变加号，替换空格为 '%20'
            chs = query.get('chs', '300x300')
            chld = query.get('chld', 'L|4')
        # print repr(chl)
        import urllib2
        chl = urllib2.unquote(chl)
        print repr(chl)
        import charset
        chl = charset.utf8(chl) # 将字符串解码然后按 utf8 编码
        print repr(chl)
        # TODO 如果编码不是 utf8，编码(quote())后重定向到 UTF8 编码后的链接
        MIME, data = self.show_image(chl, chld, chs)
        web.header('Content-Type', MIME)
        return data

    def POST(self):
        """处理 POST 数据
        """
        query = web.input(chl='', chld='L|4', chs='300x300')
        # 因为 web.input() 的返回的是 unicode 编码的数据，
        # 所以将数据按 utf8 编码以便用来生成二维码
        chl = query.chl.encode('utf8')
        chs = query.chs
        chld = query.chld
        MIME, data = self.show_image(chl, chld, chs)
        web.header('Content-Type', MIME)
        return data

if __name__ == '__main__':
    app.run()

