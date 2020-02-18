# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 20:17:09 2017

@author: lenovo
"""

class VMWriter():
    def __init__(self,output_file):
        self._output_file = output_file
        
    def writePush(self,segment,index):
        self._output_file.write('push '+str(segment)+' '+str(index)+'\n')
        
    def writePop(self,segment,index):
        self._output_file.write('pop '+str(segment)+' '+str(index)+'\n')
        
    def writeArithmetic(self,command):
        self._output_file.write(str(command)+'\n')
        
    def writeLabel(self,label):
        self._output_file.write('label {}\n'.format(str(label)))
        
    def writeGoto(self,label):
        self._output_file.write('goto {}\n'.format(label))
        
    def writeIf(self,label):
        self._output_file.write('if-goto {}\n'.format(label))
        
    def writeCall(self,name,nArgs):
        self._output_file.write('call {} {}\n'.format(name,nArgs))
        
    def writeFunction(self,name,nLocals):
        self._output_file.write('function {} {}\n'.format(name,nLocals))
        
    def writeReturn(self):
        self._output_file.write('return\n')
        
    def close(self):
        self._output_file.close()