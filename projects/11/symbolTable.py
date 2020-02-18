# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 16:38:11 2017

@author: lenovo
"""

class SymbolTable():
    def __init__(self):
        self._class_table = {}
        self._method_table = {}
        self._static_num = 0
        self._field_num = 0
        self._arg_num = 0
        self._var_num = 0
        
    def startSubroutine(self):
        self._method_table = {}
        self._arg_num = 0
        self._var_num = 0
        
    def define(self,name,typ,kind):
        if kind == 'static':
            self._class_table[name] = (typ,kind,self._static_num)
            self._static_num += 1
        elif kind == 'field':
            self._class_table[name] = (typ,kind,self._field_num)
            self._field_num += 1
        elif kind == 'var':
            self._method_table[name] = (typ,kind,self._var_num)
            self._var_num += 1
        elif kind == 'argument':
            self._method_table[name] = (typ,kind,self._arg_num)
            self._arg_num += 1
            
    def varCount(self,kind):
        if kind == 'static':
            return self._static_num
        elif kind == 'field':
            return self._field_num
        elif kind == 'var':
            return self._var_num
        elif kind == 'argument':
            return self._arg_num
        else:
            print ('not a eligable kind name')
            
    def kindOf(self,name):
        if name in self._method_table.keys():
            return self._method_table[name][1]
        elif name in self._class_table.keys():
            return self._class_table[name][1]
        else:
            return None
        
    def typeOf(self,name):
        if name in self._method_table.keys():
            return self._method_table[name][0]
        elif name in self._class_table.keys():
            return self._class_table[name][0]
        else:
            return None
        
    def indexOf(self,name):
        if name in self._method_table.keys():
            return self._method_table[name][2]
        elif name in self._class_table.keys():
            return self._class_table[name][2]
        else:
            return None
            
        