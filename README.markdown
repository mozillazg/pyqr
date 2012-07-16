# 在线生成二维码图片

## 使用技术及第三方库

* [Python 2.6](http://www.python.org/)
* [web.py]( http://webpy.org/)
* [python-qrcode](https://github.com/lincolnloop/python-qrcode)
* [PIL](http://www.pythonware.com/products/pil/index.htm)
* [SAE](http://sae.sina.com.cn/)

## 功能

在线生成二维码图片

## API

支持 GET 及 POST 请求

参数示例：

* chl='test' 二维码包含的文本信息（必需）
* chs='300x300' 图片尺寸（必需）
* chld='M|4' 纠错级别（L,M,H,Q）及二维码离图片边框的距离（非必需，默认为'M|4'）

详细 api：
[google qrcode api](https://google-developers.appspot.com/chart/infographics/docs/qr_codes)

## TODO

i18n

## Demo

<http://pyqr.sinaapp.com>

