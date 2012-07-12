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
        if len(chl) > 2953: # 最大容量
            chl = chl[:2952]
            # chl = ''
        chld = string.upper(chld) # 转换为大小字母
        if chld == '':
            chld = 'M|4'
        chld = chld.split('|') # chld 是非必需参数
        if len(chld) == 2:
            try:
                self.border = int(chld[1])
            except:
                # raise web.badrequest()
                self.version = 4
        elif len(chld) == 1:
            self.border = 4
        if chld[0] not in ['L', 'M', 'Q', 'H']:
            chld[0] = 'M'
        if self.border < 0:
            # raise web.badrequest()
            self.border = 4
        try:
            chs = string.lower(chs) # 转换为小写字母
            size = tuple([int(i) for i in chs.split('x')])
        except:
            raise web.badrequest()
        else:
            if (size[0] * size[1] == 0 or size[0] < 0 or size[1] < 0 or ( # 处理负数及零的情况
                    # size[0] < 21) or size[1] < 21 or (
                    size[0] > 500) or size[1] > 500): # 限制图片大小，防止图片太小太大导致系统死机
                raise web.badrequest()
        # self.version = 4
        self.box_size = 10
        self.size = size[0] if size[0] <= size[1] else size[1]
        # L,M,Q,H 纠错级别下 1~40 版本的最大容量(Binary)
        l_max = [17, 32, 53, 78, 106, 134, 154, 192, 230, 271, 321,
                367, 425, 458, 520, 586, 644, 718, 792, 858, 929,
                1003, 1091, 1171, 1273, 1367, 1465, 1528, 1628,
                1732, 1840, 1952, 2068, 2188, 2303, 2431, 2563,
                2699, 2809, 2953]
        m_max = [14, 26, 42, 62, 84, 106, 122, 152, 180, 213, 251,
                287, 331, 362, 412, 450, 504, 560, 624, 666, 711,
                779, 857, 911, 997, 1059, 1125, 1190, 1264, 1370,
                1452, 1538, 1628, 1722, 1809, 1911, 1989, 2099,
                2213, 2331]
        q_max = [11, 20, 32, 46, 60, 74, 86, 108, 130, 151, 177,
                203, 241, 258, 292, 322, 364, 394, 442, 482, 509,
                565, 611, 661, 715, 751, 805, 868, 908, 982, 1030,
                1112, 1168, 1228, 1283, 1351, 1423, 1499, 1579, 1663]
        h_max = [7, 14, 24, 34, 44, 58, 64, 84, 98, 119, 137, 155,
                177, 194, 220, 250, 280, 310, 338, 382, 403, 439,
                461, 511, 535, 593, 625, 658, 698, 742, 790, 842,
                898, 958, 983, 1051, 1093, 1139, 1219, 1273]
        self.level = chld[0] # 纠错级别
        # 根据纠错级别及字符数选定版本。
        if self.level == 'L':
            for i in l_max:
                if len(chl) < i:
                    self.version = l_max.index(i) + 1
                    break
            self.error_correction = qrcode.constants.ERROR_CORRECT_L
        elif self.level == 'M':
            for i in m_max:
                if len(chl) < i:
                    self.version = m_max.index(i) + 1
                    break
            self.error_correction = qrcode.constants.ERROR_CORRECT_M
        elif self.level == 'Q':
            for i in q_max:
                if len(chl) < i:
                    self.version = q_max.index(i) + 1
                    break
            self.error_correction = qrcode.constants.ERROR_CORRECT_Q
        elif self.level == 'H':
            for i in h_max:
                if len(chl) < i:
                    self.version = h_max.index(i) + 1
                    break
            self.error_correction = qrcode.constants.ERROR_CORRECT_H
        print len(chl)
        print self.version
        print self.size, self.border
        # 根据 qrcode 源码、size 及 version 参数求 box_size
        self.box_size = self.size/((self.version * 4 + 17) + self.border * 2)
        print self.box_size
        if self.box_size == 0:
            im = Image.new("1", (1, 1), "white")
        else:
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
        paste_size = ((rx-x)/2, (ry-y)/2, (rx-x)/2 + x, (ry-y)/2 + y)
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
                        query.setdefault(i[0], 'M|4')
                    elif len(i) == 2 and i[0] in ['chl', 'chs', 'chld']:
                        query.setdefault(i[0], i[1])
                # print query
            except:
                return web.badrequest()
            chl = query.get('chl', '') # TODO 必需参数不设默认值直接抛出400 error
            chl = chl.replace('+', '%20') # 解决空格变加号，替换空格为 '%20'
            chs = query.get('chs', '300x300')
            chld = query.get('chld', 'M|4')
        # print repr(chl)
        import urllib2
        chl = urllib2.unquote(chl)
        # print repr(chl)
        import charset
        chl = charset.encode(chl) # 将字符串解码然后按 utf8 编码
        # print repr(chl)
        # TODO 如果编码不是 utf8，编码(quote())后重定向到 UTF8 编码后的链接
        MIME, data = self.show_image(chl, chld, chs)
        web.header('Content-Type', MIME)
        return data

    def POST(self):
        """处理 POST 数据
        """
        query = web.input(chl='', chld='M|4', chs='300x300')
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

