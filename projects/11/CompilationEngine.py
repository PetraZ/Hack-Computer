# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 12:31:58 2017

@author: lenovo
"""
import JackTokenizer
import os
import symbolTable
import VMWriter


class CompilationEngine():
    def __init__(self,output_file,tokenizer):
        self._out_file = open(output_file,'w')
        self._tokenizer = tokenizer
        self._map = {'+':'add',
                     '-':'sub',
                     '&':'and',
                     '|':'or',
                     '<':'lt',
                     '>':'gt',
                     '=':'eq',
                     '*':'call Math.multiply 2',
                     '/':'call Math.divide 2'}
        self._unary_map = {'-':'neg',
                           '~':'not'}
        self._convert_kind = {'static':'static',
                              'argument':'argument',
                              'var':'local',
                              'field':'this'}
        self._class_name = ''
        self._table = symbolTable.SymbolTable()
        self._vmwriter = VMWriter.VMWriter(self._out_file)
        self._if_count = 0
        self._while_count = 0
    def compileClass(self):
#        self.write_nonterminal_start_tag('class')
        self.next_one() # class
        self._class_name = self.next_one() # class name
        self.next_one() # {
        
        while self.is_class_var_dec():
            self.compileClassVarDec() 
            
        while self.is_subroutine_dec():
            self.compileSubroutine()
            
            
        self.next_one() #'}'    
#        self.write_nonterminal_close_tag('class')
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
        
    def next_one(self):
        token = self._tokenizer.next_one()
#        print (token)
        return token            
    
# =============================================================================
#     def write_next_token(self):
#         token = self._tokenizer.next_one()
#         token_type = self._tokenizer.tokenType(token) 
#         if self._tokenizer.tokenType(token) == 'stringConstant':
#             token = token[1:-1]
#         if token in self._map:
#             token = self._map[token]
#                 
#         self._out_file.write('<'+token_type+'>'+token+'</'+ token_type +'>\n')
# =============================================================================
        
    def compileSubroutine(self):
#        self.write_nonterminal_start_tag('subroutineDec')
        sub_kind = self.next_one() ## constructor or function or method
        sub_type = self.next_one() # void or type
        sub_name = self.next_one() # name
        
        self._table.startSubroutine()
        if sub_kind == 'method':
            self._table.define('this',self._class_name,'argument')
            
        self.next_one() #(
        self.compileParameterList() 
        self.next_one() #')'
        
#        self.write_nonterminal_start_tag('subroutineBody')
        self.next_one()#{
        
        while self._tokenizer.browse_next() == 'var':
            self.compileVarDec()
            
        var_num = self._table.varCount('var')
        self._vmwriter.writeFunction(self._class_name+'.'+sub_name,var_num) #function xxx n_locals
        if sub_kind == 'method':
            self._vmwriter.writePush('argument',0)
            self._vmwriter.writePop('pointer',0)
        elif sub_kind == 'constructor':
            fields_num = self._table.varCount('field')
            self._vmwriter.writePush('constant',fields_num)
            self._vmwriter.writeCall('Memory.alloc',1)
            self._vmwriter.writePop('pointer',0)
        self.compileStatements()  # statements could be nothing
        self.next_one()  #}
# =============================================================================
#         if sub_type == 'void':
#             self._vmwriter.writePush('constant',0)
# =============================================================================
#        self.write_nonterminal_close_tag('subroutineBody')
#        self.write_nonterminal_close_tag('subroutineDec')
    
    def compileStatements(self):
#        self.write_nonterminal_start_tag('statements')
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
                
#        self.write_nonterminal_close_tag('statements')
        
    def compileLet(self):
#        self.write_nonterminal_start_tag('letStatement')
        ## let variable = expression
        ## or let variable[expression1] = expression2
        self.next_one() # let
        var_name = self.next_one() # var_name
        var_kind = self._convert_kind[self._table.kindOf(var_name)] ## static argument local or field(this) 
        var_index = self._table.indexOf(var_name)
        
        if self._tokenizer.browse_next() == '[':
#            print (self._tokenizer.browse_next(),1111)
            self.next_one() #[
            self._vmwriter.writePush(var_kind,var_index)
            self.compileExpression()  # push expression result onto stack
            self._vmwriter.writeArithmetic('add')
            self.next_one() #]           
            self.next_one() #=
            self.compileExpression() #push expression2 result onto stack
            self._vmwriter.writePop('temp',0)
            self._vmwriter.writePop('pointer',1)
            self._vmwriter.writePush('temp',0)
            self._vmwriter.writePop('that',0)
            self.next_one() #;
        else:
            self.next_one() # =
            self.compileExpression() # PUSH expression onto stack
#            print (self._tokenizer.browse_next())
            self._vmwriter.writePop(var_kind,var_index)
            self.next_one() #;
            
#        self.write_nonterminal_close_tag('letStatement')
        
    def compileIf(self):
#        self.write_nonterminal_start_tag('ifStatement')\\
        if_count = self._if_count ## deal with recursive call
        self._if_count += 1
        self.next_one() #if 
        self.next_one() #(
        self.compileExpression()
        self._vmwriter.writeIf('IF_TRUE'+str(if_count))
        self.next_one() #)
        self._vmwriter.writeGoto('IF_FALSE'+str(if_count))
        
        self.next_one() #{
        self._vmwriter.writeLabel('IF_TRUE'+str(if_count))
        self.compileStatements()
        self._vmwriter.writeGoto('IF_END'+str(if_count))
        self.next_one() #}
#        print (self._tokenizer.browse_next())
        
        self._vmwriter.writeLabel('IF_FALSE'+str(if_count))
        if self._tokenizer.browse_next() == 'else':
            self.next_one() #else
            self.next_one()#{
            self.compileStatements()
            self.next_one() #}
#        self.write_nonterminal_close_tag('ifStatement')        
        self._vmwriter.writeLabel('IF_END'+str(if_count))
        
        
    def compileWhile(self):
#        self.write_nonterminal_start_tag('whileStatement')
        while_count = self._while_count ## deal with the recursive call
        self._while_count += 1
        self.next_one() #while
        self.next_one() #(
        self._vmwriter.writeLabel('WHILE_START'+str(while_count))
        self.compileExpression()
        self._vmwriter.writeIf('WHILE_TRUE'+str(while_count))
        self._vmwriter.writeGoto('WHILE_END'+str(while_count))
        self.next_one() #)
        self.next_one() #{
        self._vmwriter.writeLabel('WHILE_TRUE'+str(while_count))
        self.compileStatements()
        self._vmwriter.writeGoto('WHILE_START'+str(while_count))
        self.next_one() #}
        self._vmwriter.writeLabel('WHILE_END'+str(while_count))
        
#        self.write_nonterminal_close_tag('whileStatement')
        
    def compileDo(self):
#        self.write_nonterminal_start_tag('doStatement')
        self.next_one() #do
        self.compile_subroutine_call()
        self._vmwriter.writePop('temp',0)  # do ignores the value it returned. if cares use let a = returned value
        self.next_one() #;
#        self.write_nonterminal_close_tag('doStatement')
    def compile_subroutine_call(self):
        identifier = self.next_one()## class name or instance or method or function
        kind = self._table.kindOf(identifier) # if its in table (in--instance)(not--new class)
        typ = self._table.typeOf(identifier)
        num_args = 0
        if self._tokenizer.browse_next() == '(':# its a method since function and constructors must be callled using their full name            
            fun_name = self._class_name + '.' + identifier# class.method
            num_args += 1
            self._vmwriter.writePush('pointer',0)
            
        elif self._tokenizer.browse_next() == '.': #instance or function or constructor
            if kind != None: # instance
                self.next_one() #.
                fun_name = typ + '.' + self.next_one()  # instance.method
                num_args += 1
                self._vmwriter.writePush(self._convert_kind[kind],self._table.indexOf(identifier)) # instance this
            else:
                self.next_one() #.
                fun_name = identifier + '.' + self.next_one()
        self.next_one() #(
        num_args += self.compileExpressionList()  
        self.next_one() #)
        
        self._vmwriter.writeCall(fun_name,num_args)
            

            
    def compileReturn(self):
#        self.write_nonterminal_start_tag('returnStatement')
        self.next_one() #return
        if self._tokenizer.browse_next() == ';':
            self._vmwriter.writePush('constant',0)
            self._vmwriter.writeReturn()

        else:
            self.compileExpression()
            self._vmwriter.writeReturn()
             
        self.next_one() #;
        
#        self.write_nonterminal_close_tag('returnStatement')
        
    def compileExpression(self):
#        self.write_nonterminal_start_tag('expression')
        self.compileTerm() #term
        
        while self._tokenizer.browse_next() in '+|-|*|/|&|||<|>|=':
            op = self.next_one() # op + - * / & | < > =
            self.compileTerm()
            self._vmwriter.writeArithmetic(self._map[op])
#        self.write_nonterminal_close_tag('expression')
      
    def compileTerm(self):
#        self.write_nonterminal_start_tag('term')
#        print (self._tokenizer.browse_next())
        if self._tokenizer.browse_next() in '-|~':
#            print (self._tokenizer.browse_next(),66666)
            unary_op = self.next_one() # unary op 
            self.compileTerm()
            self._vmwriter.writeArithmetic(self._unary_map[unary_op])
            
        elif self._tokenizer.browse_next() == '(':
            self.next_one() #(
            self.compileExpression()
            self.next_one() #)
            
        elif self._tokenizer.browse_next().isdigit():
            cons = self.next_one()
#            print (cons,2333)
            self._vmwriter.writePush('constant',cons)
            
        elif self._tokenizer.tokenType(self._tokenizer.browse_next()) == 'stringConstant':
#            print(444)
            self.compileStringConstant()  ## push 
            
        elif self._tokenizer.browse_next() in ['true','false','null','this']:
#            print (self._tokenizer.browse_next(),64446)
            self.compileKeywordConstant()
        
        else:  #varname , varname[] or subroutine call
#            print (self._tokenizer.browse_next(2),555555)
            if self._tokenizer.browse_next(2) == '[':
                name = self.next_one()
#                print (name,222)
                kind = self._convert_kind[self._table.kindOf(name)]
                index = self._table.indexOf(name)
                self.next_one() #[
                self.compileExpression() # push result onto stack
                self.next_one() #]
                self._vmwriter.writePush(kind,index)
                self._vmwriter.writeArithmetic('add')
                self._vmwriter.writePop('pointer',1)
                self._vmwriter.writePush('that',0)
                
                
            elif self._tokenizer.browse_next(2) in '(|.': # must be a subroutine call
                self.compile_subroutine_call()
                
            else: #var
                var_name = self.next_one()
#                print (var_name,222)
                kind = self._convert_kind[self._table.kindOf(var_name)]
                index = self._table.indexOf(var_name)
                self._vmwriter.writePush(kind,index)
                
            
# =============================================================================
#         kind = self._table.kindOf(name)
#         if kind == None :
#             return True
#         else:
#             return False
# =============================================================================
    def compileStringConstant(self):
        string = self.next_one()[1:-1] ## "sdf" to sdf
        
        self._vmwriter.writePush('constant',len(string)) 
        self._vmwriter.writeCall('String.new',1) #1 arg
        
        for character in string :
            self._vmwriter.writePush('constant',ord(character))
            self._vmwriter.writeCall('String.appendChar',2) #its a method compiled down should be 1+1 args
            
    def compileKeywordConstant(self):
        keyword_constant = self.next_one()
        if keyword_constant == 'this':
            self._vmwriter.writePush('pointer',0)  # just lake a number
        elif keyword_constant == 'true':
            self._vmwriter.writePush('constant',0) # -1 does not work probabaly no address like that
            self._vmwriter.writeArithmetic('not')
        else :
            self._vmwriter.writePush('constant',0)
            
    def compileExpressionList(self):
#        self.write_nonterminal_start_tag('expressionList')
        num_args = 0
        if self._tokenizer.browse_next() != ')':
            self.compileExpression()
            num_args += 1
        
        while self._tokenizer.browse_next() == ',':
            self.next_one() #,
            self.compileExpression()
            num_args += 1
        return num_args
#        self.write_nonterminal_close_tag('expressionList')
        
    def compileVarDec(self):
#        self.write_nonterminal_start_tag('varDec')
        self.next_one()  # var
        var_type = self.next_one()  # type
        var_name = self.next_one()  # var_name
        self._table.define(var_name,var_type,'var')
        
        while self._tokenizer.browse_next() != ';':
            self.next_one() # ,
            var_name = self.next_one() # var-name
            self._table.define(var_name,var_type,'var')

        self.next_one()  # ;
#        self.write_nonterminal_close_tag('varDec')

    def compileParameterList(self):
#        self.write_nonterminal_start_tag('parameterList')
        if self._tokenizer.browse_next() != ')':
            arg_type = self.next_one()  # type
            arg_name = self.next_one()  # arg name
            self._table.define(arg_name,arg_type,'argument')
            
        while self._tokenizer.browse_next() != ')':
            self.next_one() #,
            arg_type = self.next_one() #type int boolean
            arg_name = self.next_one() # arg name
            self._table.define(arg_name,arg_type,'argument')
#        self.write_nonterminal_close_tag('parameterList')
        
        
    def compileClassVarDec(self):
#        self.write_nonterminal_start_tag('classVarDec')
        kind = self.next_one() #(static or field)
        typ = self.next_one()  # type(int boolean or string)
        name = self.next_one()  # var name
        self._table.define(name,typ,kind)
        while self._tokenizer.browse_next() != ';':
            self.next_one()  # ,
            name = self.next_one()  # var name
            self._table.define(name,typ,kind)
            
        self.next_one()   #;
#        self.write_nonterminal_close_tag('classVarDec')
        
# =============================================================================
# file = os.getcwd()
# input_file = file + '\Main.jack'
# output_file = file + '\Main.vm'
# a = JackTokenizer.JackTokenizer(input_file)
# a.tokenize_all()
# #print(a._tokens)
# # 
# b = CompilationEngine(output_file,a)
# b.compileClass()
# #    
# =============================================================================
