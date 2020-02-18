# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 19:21:46 2017

@author: lenovo
"""
import re
import Lexical
import os 

class JackTokenizer():
    def __init__(self,input_file):
        self._file_name = input_file
        self._input_file = open(input_file)        
        self._lines = []
        self._tokens = []
        self._length = 0
        self._index = -1
        self._current_token = ''
        
    def cleanComment(self):
        file = self._input_file.readlines()
        
        for line in file:
            if line.strip().startswith('*') or line.strip().startswith('/*'):
                continue
            line_content = line.split('//')[0].strip()
            if  line_content == '' :
                continue
            else:
                self._lines.append(line_content)
                
    def tokenize(self):
        string_const = False
        a_string = None
        for cleaned_line in self._lines:
            temp = cleaned_line.split('\n')[0].split()
            for element in temp:
                tokens = re.split('('+Lexical.symbols+')\s*',element)
                for token in tokens:
                    if token != '':
                        if string_const:
                            if token.endswith('"'):
                                a_string += token
                                self._tokens.append(a_string)
                                a_string = ''
                                string_const = False
                            else:
                                a_string += token
                                
                        elif token.startswith('"'):
                            string_const = True
                            a_string = token
                        else:     
                            self._tokens.append(token)
                        
        self._length = len(self._tokens)      
        
    def hasMoreTokens(self):
        if self._index >= self._length:
            return False
        else :
            return True
        
    def browse_next(self):
        if self._index < self._length:
            return self._tokens[self._index+1]
        else:
            print ('browsing not in range')
            return self._current_token
        
    def advance(self):
        if self.hasMoreTokens():
            self._index += 1
            self._current_token = self._tokens[self._index]
            
            return self._current_token
                
    def backward(self):
        if self._index > 0:
            self._index -= 1
            
    def tokenType(self):
        if self._current_token in Lexical.symbol_list:
            return 'SYMBOL'
        elif self._current_token in Lexical.key_words_list:
            return 'KEYWORD'
        elif self._current_token.startswith('"'):
            return 'STRING'
        elif self._current_token.isdigit():
            return 'CONSTANT'
        else :
            return 'INDENTIFIER'
        
    def writeOutFile(self):
        self.cleanComment()
        self.tokenize()
        out_file = open(self._file_name[:-5]+'T.xml','w')
        out_file.write('<tokens>\n')
  
        for token in range(self._length):
            self.advance()
            out_file.write('<'+self.tokenType()+'>'+self._current_token+'</'+self.tokenType()+'>\n')
#            print (token)
            
        out_file.write('</tokens>\n')
        out_file.close()
        self._index = 0
            
file = os.getcwd()
file = file + '\Main.jack'
a = JackTokenizer(file)
#a.cleanComment()
#a.tokenize()
a.writeOutFile()
# =============================================================================
# for i in range(10):
#     print (a.advance())
#     print (a.tokenType())
# =============================================================================


