#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""简单猜测字符编码并返回经过utf8编码的字符
"""

def utf8(stri):
    charests = ('utf8', 'gbk', 'gb2312', 'big5', 'ascii',
                'shift_jis', 'euc_jp', 'euc_kr', 'iso2022_kr', 'latin1', 'latin2', 'latin9', 'latin10', 'koi8_r', 'cyrillic', 'utf16', 'utf32'
                 )
    str_ = stri
    for i in charests:
        try:
            str_ = stri.decode(i).encode('utf8')
            break
        except:
            pass
    return str_

