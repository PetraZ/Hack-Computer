# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 12:31:58 2017

@author: lenovo
"""
import JackTokenizer
import os

class CompilationEngine():
    def __init__(self,output_file,tokenizer):
        self._out_file = open(output_file,'w')
        self._tokenizer = tokenizer
        self._map = {'<':'&lt;',
                     '>':'&gt;',
                     '"':'&quot;',
                     '&':'&amp;'}
    
    def compileClass(self):
        self.write_nonterminal_start_tag('class')
        self.write_next_token() # class
        self.write_next_token() # class name
        self.write_next_token() # {
        while self.is_class_var_dec():
            self.compileClassVarDec() 
            
        while self.is_subroutine_dec():
            self.compileSubroutine()
            
            
        self.write_next_token() #'}'    
        self.write_nonterminal_close_tag('class')
        self._out_file.close()
        
    def is_class_var_dec(self):
        next_token = self._tokenizer.browse_next()
        if  next_token in ('static','field'):
            return True
        else:
            return False
        
    def is_subroutine_dec(self):
        next_token = self._tokenizer.browse_next()
        if next_token in ('constructor','function','method'):
            return True
        else:
            return False
        
    def write_nonterminal_start_tag(self,name):
        self._out_file.write('<'+str(name)+'>\n')
        
    def write_nonterminal_close_tag(self,name):
        self._out_file.write('</'+str(name)+'>\n')
                
    def write_next_token(self):
        token = self._tokenizer.next_one()
        token_type = self._tokenizer.tokenType(token) 
        if self._tokenizer.tokenType(token) == 'stringConstant':
            token = token[1:-1]
        if token in self._map:
            token = self._map[token]
                
        self._out_file.write('<'+token_type+'>'+token+'</'+ token_type +'>\n')
        
    def compileSubroutine(self):
        self.write_nonterminal_start_tag('subroutineDec')
        self.write_next_token() ## constructor or function or method
        self.write_next_token() #void or type
        self.write_next_token() # name
        self.write_next_token() #(
        self.compileParameterList() 
        self.write_next_token() #')'
        
        self.write_nonterminal_start_tag('subroutineBody')
        self.write_next_token() #{
        
        while self._tokenizer.browse_next() == 'var':
            self.compileVarDec()
        
        self.compileStatements()  # statements could be nothing
        self.write_next_token()  #}
        self.write_nonterminal_close_tag('subroutineBody')
        self.write_nonterminal_close_tag('subroutineDec')
    
    def compileStatements(self):
        self.write_nonterminal_start_tag('statements')
        while self._tokenizer.browse_next() in ('let','if','while','do','return'):
            next_token = self._tokenizer.browse_next()
            if next_token == 'let':
                self.compileLet()
            elif next_token == 'if':
                self.compileIf()
            elif next_token == 'while':
                self.compileWhile()
            elif next_token == 'do':
                self.compileDo()
            elif next_token == 'return':
                self.compileReturn()
                
        self.write_nonterminal_close_tag('statements')
        
    def compileLet(self):
        self.write_nonterminal_start_tag('letStatement')
        self.write_next_token() # let
        self.write_next_token() # var_name
        if self._tokenizer.browse_next() == '[':
            self.write_next_token() #[
            self.compileExpression()
            self.write_next_token() #]
        self.write_next_token() #=
        self.compileExpression()
        self.write_next_token() #;
        self.write_nonterminal_close_tag('letStatement')
        
    def compileIf(self):
        self.write_nonterminal_start_tag('ifStatement')
        self.write_next_token() #if
        self.write_next_token() #(
        self.compileExpression()
        self.write_next_token() #)
        self.write_next_token() #{
        self.compileStatements()
        self.write_next_token() #}
        print (self._tokenizer.browse_next())
        if self._tokenizer.browse_next() == 'else':
            self.write_next_token() #else
            self.write_next_token() #{
            self.compileStatements()
            self.write_next_token() #}
        self.write_nonterminal_close_tag('ifStatement')
        
    def compileWhile(self):
        self.write_nonterminal_start_tag('whileStatement')
        self.write_next_token() #while
        self.write_next_token() #(
        self.compileExpression()
        self.write_next_token() #)
        self.write_next_token() #{
        self.compileStatements()
        self.write_next_token() #}
        self.write_nonterminal_close_tag('whileStatement')
        
    def compileDo(self):
        self.write_nonterminal_start_tag('doStatement')
        self.write_next_token() #do
        self.write_next_token() #function or method or class name
        
        if self._tokenizer.browse_next() == '.':
            self.write_next_token() #.
            self.write_next_token() #function or method
            
        self.write_next_token() #(
        self.compileExpressionList()
        self.write_next_token() #)
        self.write_next_token() #;
        self.write_nonterminal_close_tag('doStatement')
        
    def compileReturn(self):
        self.write_nonterminal_start_tag('returnStatement')
        self.write_next_token() #return
        if self._tokenizer.browse_next() == ';':
            self.write_next_token() #;
        else:
            self.compileExpression()
            self.write_next_token() #;
        
        self.write_nonterminal_close_tag('returnStatement')
        
    def compileExpression(self):
        self.write_nonterminal_start_tag('expression')
        self.compileTerm() #term
        
        while self._tokenizer.browse_next() in '+|-|*|/|&|||<|>|=':
            self.write_next_token() # op + - * / & | < > =
            self.compileTerm()
            
        self.write_nonterminal_close_tag('expression')
        
    def compileTerm(self):
        self.write_nonterminal_start_tag('term')
        
        if self._tokenizer.browse_next() in '-|~':
            self.write_next_token() # unary op 
            self.compileTerm()
        elif self._tokenizer.browse_next() == '(':
            self.write_next_token() #(
            self.compileExpression()
            self.write_next_token() #)
        else:
            self.write_next_token() # idenfitifier or number
            
            if self._tokenizer.browse_next() == '(':
                self.write_next_token() #(
                self.compileExpressionList()
                self.write_next_token() #)
            elif self._tokenizer.browse_next() == '.':
                self.write_next_token() #.
                self.write_next_token() #sub name
                self.write_next_token() #(
                self.compileExpressionList()
                self.write_next_token() #)
            elif self._tokenizer.browse_next() == '[':
                self.write_next_token() #[
                self.compileExpression()
                self.write_next_token() #]
        
        self.write_nonterminal_close_tag('term')
    def compileExpressionList(self):
        self.write_nonterminal_start_tag('expressionList')
        
        if self._tokenizer.browse_next() != ')':
            self.compileExpression()
        
        while self._tokenizer.browse_next() == ',':
            self.write_next_token() #,
            self.compileExpression()
        self.write_nonterminal_close_tag('expressionList')
    def compileVarDec(self):
        self.write_nonterminal_start_tag('varDec')
        self.write_next_token()  # var
        self.write_next_token()  # type
        self.write_next_token()  # var_name

        while self._tokenizer.browse_next() != ';':
            self.write_next_token() # ,
            self.write_next_token() # var-name
        self.write_next_token()  # ;
        self.write_nonterminal_close_tag('varDec')
    
    def compileParameterList(self):
        self.write_nonterminal_start_tag('parameterList')
        while self._tokenizer.browse_next() != ')':
            self.write_next_token()
            
        self.write_nonterminal_close_tag('parameterList')
        
        
    def compileClassVarDec(self):
        self.write_nonterminal_start_tag('classVarDec')
        self.write_next_token()  #(static or filed)
        self.write_next_token()  # type(int boolean or string)
        self.write_next_token()  # var name
        
        while self._tokenizer.browse_next() != ';':
            self.write_next_token()  # ,
            self.write_next_token()  # var name
            
        self.write_next_token()   #;
        self.write_nonterminal_close_tag('classVarDec')
        
#file = os.getcwd()
#input_file = file + '\Main.jack'
#output_file = file + '\Main.xml'
#a = JackTokenizer.JackTokenizer(input_file)
#a.tokenize_all()
# 
#b = CompilationEngine(output_file,a)
#b.compileClass()
#    