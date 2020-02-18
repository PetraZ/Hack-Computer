# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 11:53:31 2017

@author: lenovo
"""
import JackTokenizer
import CompilationEngine
import os
def main():
    for (dirpath,dirname,filename) in os.walk('./'):
        for file in filename:
            if file.endswith('.jack'):
                
                jack_path = os.path.join(dirpath,file).replace('\\','/')
                print (jack_path)
                a = JackTokenizer.JackTokenizer(jack_path)
                a.writeOutFile()
                output_file = jack_path[:-5]+'.xml'
                b = CompilationEngine.CompilationEngine(output_file,a)
                b.compileClass()
    
                
main()