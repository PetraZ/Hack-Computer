# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 16:31:14 2017

@author: lenovo
"""
import Lexical,os


class JackTokenizer():
    def __init__(self,input_file):
        self._file_name = input_file
        self._input_file = open(input_file)        
        self._tokens = []
        self._length = 0
        self._index = -1
        self._current_token = ''
        self._map = {'<':'&lt;',
                     '>':'&gt;',
                     '"':'&quot;',
                     '&':'&amp;'}
        
    def hasMoreTokens(self):
        if self.peekNextCharater() == '' :
            return False
        else:
            return True
        
    def tokenize_all(self):
        self._input_file.seek(0)
#        print (self.getNextWord())
        while self.hasMoreTokens():
            next_word = self.getNextWord()
            if next_word != '':
                self._tokens.append(next_word)
        self._length = len(self._tokens)
        self._index = -1
    
    def browse_next(self,num=1):
        if (self._index+num) < self._length:
            return self._tokens[self._index+num]
        else:
            print ('browsing not in range')
            return self._current_token
        
    def next_one(self):
        if self._index < (self._length-1):
            self._index += 1
            self._current_token = self._tokens[self._index]            
            return self._current_token 
        
    def advance(self):
        if self.hasMoreTokens():
            current_token = self.getNextWord()
        return current_token
    
    def tokenType(self,token):
        if token in Lexical.symbol_list:
            return 'symbol'
        elif token in Lexical.key_words_list:
            return 'keyword'
        elif token.startswith('"'):
            return 'stringConstant'
        elif token.isdigit():
            return 'integerConstant'
        else :
            return 'identifier'            
        
    def getNextWord(self):
        word = ''
        if self.peekNextCharater(2) == '//':
            self.read(2)
#            print (1)
            while self.peekNextCharater() != '\n':
                self.read()
            self.read()
            word = self.getNextWord()
            
        elif self.peekNextCharater(2) == '/*':
#            self.read(2)
            while self.peekNextCharater(2) != '*/':
                self.read() 
            self.read(2)
            word = self.getNextWord()
            
        elif self.peekNextCharater() == '"':
            self.read()
            word += '"'
            while self.peekNextCharater() != '"':
                word += self.read() 
            self.read() #"
            word += '"'
            
        elif self.peekNextCharater() in Lexical.while_space:
            self.read()
#            print (3)
            word = self.getNextWord()
            
        elif self.peekNextCharater() in Lexical.symbol_list:
#            print (5)
#            print (self.peekNextCharater() )
            word = self.read()
        elif self.peekNextCharater() == '':
            word = ''
#            print ('stop')
        else:        
#            print (2)
            while self.peekNextCharater() not in (Lexical.symbol_list+Lexical.while_space):
#                print (33)
                word += self.read()
#        print (word)     
        return word
        
    def read(self,num = 1):
        self._index += num
        return self._input_file.read(num)
        
    def peekNextCharater(self,num = 1):
        '''browse next charater 
        '''
        pos = self._input_file.tell()
        charater = self._input_file.read(num)
        self._input_file.seek(pos)
        return charater
        
    def writeOutFile(self):
        out_file = open(self._file_name[:-5]+'T.xml','w')
        out_file.write('<tokens>\n')
        self.tokenize_all()
#        print (self._length)
#        print (self._tokens)
        for token in self._tokens:
            token_type = self.tokenType(token)
            if self.tokenType(token) == 'stringConstant':
                token = token[1:-1]        
            if token in self._map:
                token = self._map[token]
#            print (token)
            out_file.write('<'+token_type+'>'+token+'</'+token_type+'>\n')
                
#            print (token)
            
        out_file.write('</tokens>\n')
        out_file.close()
        
# =============================================================================
# file = os.getcwd()
# file = file + '\Main.jack'
# a = JackTokenizer(file)
# 
# a.writeOutFile()       
# =============================================================================
#file = os.getcwd()
#input_file = file + '\Main.jack'
#while a.hasMoreTokens():
##    print (a.hasMoreTokens())
#    print (a.advance())

