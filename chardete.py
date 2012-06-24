#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""简单猜测字符编码并返回经过utf8编码的字符
"""

def dete(stri):
    charests = ('utf8', 'gbk', 'big5', 'gb2312',
                 'jp', 'euc_kr', 'utf16', 'utf32')
    str_ = stri
    for i in charests:
        try:
            str_ = stri.decode(i).encode('utf8')
            break
        except:
            pass
    return str_

