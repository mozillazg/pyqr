#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""简单猜测字符串编码并返回重新经过编码（默认utf8）的字符串
"""

def encode(stri, encoding='utf8'):
    charests = ('utf8', 'gbk', 'gb2312', 'big5', 'ascii',
                'shift_jis', 'euc_jp', 'euc_kr', 'iso2022_kr',
                'latin1', 'latin2', 'latin9', 'latin10', 'koi8_r',
                'cyrillic', 'utf16', 'utf32'
                 )
    if isinstance(stri, unicode):
        return stri.encode(encoding)
    else:
        for i in charests:
            try:
                return stri.decode(i).encode(encoding)
                break
            except:
                pass
        else:
            return None

