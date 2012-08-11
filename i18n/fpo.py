#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""处理 po 文件
"""

import fnmatch
import os
import charset

def files(dirpath):
    
    for file in os.listdir(dirpath):
        if fnmatch.fnmatch(file, '*.po'):
            yield file

def po(files):
    
    for file in files:
        fil_b = open(file).read()
        fil_b = fil_b.replace('CHARSET', 'utf-8')
        fil_b = fil_b.replace('ENCODING', 'utf-8')
        fil_b = charset.encode(fil_b)
        open(file, 'w').write(fil_b)

if __name__ == '__main__':
    po(files('.'))
    raw_input('Enter')
    
