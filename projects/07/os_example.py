# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 23:53:11 2017

@author: lenovo
"""
import os

n = 0
vm_files_lst = []
for root, dirs, files in os.walk('./'):
    for name in files:
        if(name.endswith(".vm")):
            n += 1
            vm_files_lst.append( os.path.join(root, name))
            print os.path.join(root, name)[:-2]