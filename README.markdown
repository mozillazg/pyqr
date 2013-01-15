# 在线生成二维码图片

## 使用技术及第三方库

* [Python 2.6](http://www.python.org/)
* [web.py]( http://webpy.org/)
* [python-qrcode](https://github.com/lincolnloop/python-qrcode)
* [PIL](http://www.pythonware.com/products/pil/index.htm)

## 功能

在线生成二维码图片

## API

支持 GET 及 POST 请求

<http://qr.3sd.me/qr?chl=hello+world&chs=350x350&chld=M|6>

* chl: 二维码包含的文本信息（必需）
* chs: 图片尺寸（必需）
* chld: 纠错级别（L(7%),M(15%),Q(25%),H(30%)）及二维码离图片边框的距离（非必需，默认为'M|4'）

## Demo

<http://qr.3sd.me>

