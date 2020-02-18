# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 14:26:18 2017

@author: lenovo
"""

import os 

a = open('123.txt','a')


print a.tell()

a.write('aaaaaaaaa\n')
a.close()