#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 判断图片 MIME 类型
usage:

>> mime = ImageMIME().get_mime(binary)

binary: utf8 编码的图片内容
mime: 图片 MIME 类型，类似"image/png"
"""

class ImageMIME(object):
    """判断图片 MIME 类型
    """
    def __init__(self):
        self.GIF = "image/gif"
        self.JPEG = "image/jpeg"
        self.TIFF = "image/tiff"
        self.PNG = "image/png"
        self.BMP = "image/bmp"
        self.ICO = "image/x-icon"
        self.UNKNOWN = "application/octet-stream"

    def get_mime(self, binary):
        size = len(binary)
        if size >= 6 and binary.startswith("GIF"):
            return self.GIF
        elif size >= 8 and binary.startswith("\x89PNG\x0D\x0A\x1A\x0A"):
            return self.PNG
        elif size >= 2 and binary.startswith("\xff\xD8"):
            return self.JPEG
        elif (size >= 6 and (binary.startswith("II*\x00") or
                             binary.startswith("MM\x00*")
                             )):
            return self.TIFF
        elif size >= 2 and binary.startswith("BM"):
            return self.BMP
        elif size >= 4 and binary.startswith("\x00\x00\x01\x00"):
            return self.ICO
        else:
            return self.UNKNOWN
