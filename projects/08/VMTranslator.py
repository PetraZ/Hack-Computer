# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 11:19:29 2017

@author: YIANG
REWRITE THE VM translator
"""
import os

class Parser():
    def __init__(self,input_file):
        self.infile = open(input_file)
        self.command = ['abcd']
        self.advance_stop_flag = False
        
        self.c_type = {
                       'add'  : 'math',
                       'sub'  : 'math',
                       'neg'  : 'math',
                       'eq'   : 'math',
                       'gt'   : 'math',
                       'lt'   : 'math',
                       'and'  : 'math',
                       'or'   : 'math',
                       'not'  : 'math',
                       'push' : 'push',
                       'pop'  : 'pop' ,
                       'label': 'label',
                       'goto' : 'goto',
                       'if-goto'   : 'if',
                       'call' : 'call',
                       'return': 'return',
                       'function':'function',
                       
                       }
                      
    def hasMoreCommands(self):
        position = self.infile.tell()
        self.advance()
        self.infile.seek(position)
        return (not self.advance_stop_flag)
        
    
    def advance(self):
        current_line = self.infile.readline()
        if current_line == '':
            self.advance_stop_flag = True
        else:
            split_line = current_line.split('/')[0].strip()
            if split_line == '':
                self.advance()
            else:
                self.command = split_line.split()
                
    def commandType(self):
        return self.c_type.get(self.command[0],'invalid c_type')
        
    def arg1(self):
        return self.command[1]

    def arg2(self):
        return self.command[2]
                
class CodeWriter():
    def __init__(self,dest,label_counter=0,vm_file_path=None):
        self.root = vm_file_path[:-3].split('/')[-1]
#        print self.root
        self.outfile = open(dest,'a')
        self.label_number = label_counter
    def get_label_counter(self):
        return self.label_number
    def writer_close(self):
        self.outfile.close()
    def set_file_name(self,file_name):
        self.file_name = file_name
        
        
    def write_label (self,label_string):
        asm = '('+str(label_string)+')'+'\n'
        self.outfile.write('//label'+str(label_string)+'\n'+asm)

        
    def write_goto(self,label):
        asm = ('@'+str(label)+'\n'+
               '0;JMP'+'\n')
        self.outfile.write('//goto'+'label'+str(label)+'\n'+asm)
        
    def write_if(self,label):
        asm = ('@SP'+'\n'
               'AM=M-1'+'\n'
               'D=M'+'\n'
               '@'+str(label)+'\n'
               'D;JNE\n'
               )
        self.outfile.write('//if_goto'+'label'+str(label)+'\n'+asm)
        
    def write_init(self):
        asm = ('@256\n'+
               'D=A\n'+
               '@SP\n'+
               'M=D\n')
        self.outfile.write('//write init function\n' + asm)
        self.write_call('Sys.init',0)
        
    def write_call(self,function_name,num_args):
        asm = ('@'+str(function_name)+'.return'+str(self.label_number)+'\n'+
               'D=A\n'+
               '@SP\n'+
               'A=M\n'+
               'M=D\n'+
               '@SP\n'+
               'M=M+1\n'+                 ## PUSH RETURN ADDRESS ONTO STACK
               
              '@LCL\n'+
              'D=M\n'+
              '@SP\n'+
              'A=M\n'+
              'M=D\n'+
              '@SP\n'+
              'M=M+1\n'+               ## PUSH LCL ADDRESS ONTO STACK
              
              '@ARG\n'+
              'D=M\n'+
              '@SP\n'+
              'A=M\n'+
              'M=D\n'+
              '@SP\n'+
              'M=M+1\n'+               ## PUSH ARG ADDRESS ONTO STACK
              
              '@THIS\n'+
              'D=M\n'+
              '@SP\n'+
              'A=M\n'+
              'M=D\n'+
              '@SP\n'+
              'M=M+1\n'+               ## PUSH THIS ADDRESS ONTO STACK
              
              '@THAT\n'+
              'D=M\n'+
              '@SP\n'+
              'A=M\n'+
              'M=D\n'+
              '@SP\n'+
              'M=M+1\n'+               ## PUSH THAT ADDRESS ONTO STACK
              
              '@SP\n'+
              'D=M\n'+
              '@'+str(num_args)+'\n'+
              'D=D-A\n'+
              '@R5\n'+
              'D=D-A\n'+
              '@ARG\n'+
              'M=D\n'+              ##REPOSITION ARG 
              
              '@SP\n'+
              'D=M\n'+
              '@LCL\n'
              'M=D\n'+             ## reposition LCL
              
              '@'+str(function_name)+'\n'+
              '0;JMP\n'+
              '('+str(function_name)+'.return'+str(self.label_number)+')'+'\n')
        self.label_number += 1
        self.outfile.write('//'+'call'+str(function_name)+str(num_args)+'\n'+asm)
         
    def write_return(self):
        asm =(
              '@LCL'+'\n'
              'D=M'+'\n'
              '@R13'+'\n'   ##R13 is  tempera var as FRAME
              'M=D'+'\n'    ## store LCL address in FRAME(@R13)
              
              '@R5'+'\n'
              'D=D-A'+'\n'     #'LCL' address
              'A=D'+'\n'
              'D=M'+'\n'
              '@R14'+'\n'  ##R14 as a temp var for Return
              'M=D'+'\n'
              
              '@SP'+'\n'     ##the function has finished and now the return value
              'A=M-1'+'\n'              ##is at the topmost in the stack SP-1
              'D=M'+'\n'
              '@ARG'+'\n'
              'A=M'+'\n'
              'M=D'+'\n'       ## PUT RETURN VALUE AT ARG POSITION (return stack point)
              
              '@ARG'+'\n'
              'D=M+1'+'\n'
              '@SP'+'\n'
              'M=D'+'\n'      ##SP=ARG+1
              
              '@13'+'\n'
              'AM=M-1'+'\n'
              'D=M'+'\n'
              '@THAT'+'\n'
              'M=D'+'\n'    ## THAT=(FRAME-1) (FRAME HAS BEEN DECERASED ONE HERE)
              
              '@13'+'\n'
              'AM=M-1'+'\n'
              'D=M'+'\n'
              '@THIS'+'\n'
              'M=D'+'\n'
              
              '@13'+'\n'
              'AM=M-1'+'\n'
              'D=M'+'\n'
              '@ARG'+'\n'
              'M=D'+'\n'
              
              '@13'+'\n'
              'AM=M-1'+'\n'
              'D=M'+'\n'
              '@LCL'+'\n'
              'M=D'+'\n'
              
              '@14'+'\n'
              'A=M'+'\n'
              '0;JMP\n'    ## goto return point of ROM
              )
        self.outfile.write('//return\n'+asm)  
        
    def write_function(self,function_name,num_locals):
        asm = '('+str(function_name)+')'+'\n'
        num_loop = int(num_locals)
        while num_loop > 0:
            asm += ('@0\n'+
                    'D=A\n'+
                    '@SP\n'+
                    'A=M\n'+
                    'M=D\n'+
                    '@SP\n'+
                    'M=M+1\n'
                    )
            num_loop -= 1
        self.outfile.write('// declare a function' +str(function_name)+'with'+str(num_locals)+'locals'+'\n'+asm)
    def write_arithmetric(self,command):
        asm = ''
        if command == 'add':
            asm=('@SP'+'\n'+         
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'M=M+D'+'\n')
            
        elif command == 'sub':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'M=M-D'+'\n')
            
        elif command == 'neg':
            asm=('@SP'+'\n'+
                'A=M-1'+'\n'+
                'M=-M'+'\n')
            
        elif command == 'not' :
            asm=('@SP'+'\n'+
                'A=M-1'+'\n'+
                'M=!M'+'\n')
            
        elif command == 'or':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'M=D|M'+'\n')
        
        elif command == 'and':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'M=M&D'+'\n')
            
        elif command == 'eq':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'D=M-D'+'\n'+      # do the subtraction   
                'M=-1'+'\n'+
                '@eq_true'+str(self.label_number)+'\n'+
                'D;JEQ'+'\n'+
                '@SP'+'\n'+
                'A=M-1'+'\n'+
                'M=0'+'\n'+
                '(eq_true'+str(self.label_number)+')'+'\n')
            self.label_number += 1    
        elif command == 'gt':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'D=M-D'+'\n'+     # do the same subtraction
                'M=-1'+'\n'+      # first assume it is true
                '@gt_true'+str(self.label_number)+'\n'+
                'D;JGT'+'\n'+
                '@SP'+'\n'+
                'A=M-1'+'\n'+
                'M=0'+'\n'+
                '(gt_true'+str(self.label_number)+')'+'\n')
            self.label_number += 1
            
        elif command == 'lt':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'D=M-D'+'\n'+     # do the same subtraction
                'M=-1'+'\n'+
                '@lt_true'+str(self.label_number)+'\n'+
                'D;JLT'+'\n'+
                '@SP'+'\n'+
                'A=M-1'+'\n'+
                'M=0'+'\n'+
                '(lt_true'+str(self.label_number)+')'+'\n')
            self.label_number += 1
    
        self.outfile.write('//'+command+'\n'+asm)
        

        
                
    def write_push_pop(self,command,segment,index):
        ''' command is ctype ,
            segment is first argument
            index is second
        '''
        asm = ''
        if command == 'push':
            if segment == 'constant':
                asm= ('@'+index+'\n'+
                 'D=A'+'\n'+
                 '@SP'+'\n'+
                 'A=M'+'\n'+
                 'M=D'+'\n'+
                 '@SP'+'\n'+
                 'M=M+1'+'\n')
                
            elif segment == 'this':
                asm=('@THIS'+'\n'+
                    'D=M'+'\n'+
                    '@'+index+'\n'+
                    'A=D+A'+'\n'+
                    'D=M'+'\n'+
                    '@SP'+'\n'+
                    'A=M'+'\n'+
                    'M=D'+'\n'+
                    '@SP'+'\n'+
                    'M=M+1'+'\n')
                
            elif segment == 'that':
                asm=('@THAT'+'\n'+
                'D=M'+'\n'+
                '@'+index+'\n'+
                'A=D+A'+'\n'+
                'D=M'+'\n'+
                '@SP'+'\n'+    ## push back to stack
                'A=M'+'\n'+
                'M=D'+'\n'+
                '@SP'+'\n'+
                'M=M+1'+'\n')
                
            elif segment == 'argument':
                asm=('@ARG'+'\n'+
                'D=M'+'\n'+
                '@'+index+'\n'+
                'A=D+A'+'\n'+
                'D=M'+'\n'+
                '@SP'+'\n'+    ## push back to stack
                'A=M'+'\n'+
                'M=D'+'\n'+
                '@SP'+'\n'+
                'M=M+1'+'\n')
                
            elif segment == 'local':
                asm=('@LCL'+'\n'+
                'D=M'+'\n'+
                '@'+index+'\n'+
                'A=D+A'+'\n'+
                'D=M'+'\n'+
                '@SP'+'\n'+    ## push back to stack
                'A=M'+'\n'+
                'M=D'+'\n'+
                '@SP'+'\n'+
                'M=M+1'+'\n')
                
            elif segment == 'temp':
                asm=('@R5'+'\n'+   # base address of eight temp memories.
                'D=A'+'\n'+
                '@'+index+'\n'+
                'A=D+A'+'\n'+
                'D=M'+'\n'+
                '@SP'+'\n'+    ## push back to stack
                'A=M'+'\n'+
                'M=D'+'\n'+
                '@SP'+'\n'+
                'M=M+1'+'\n')
                
            elif segment == 'pointer':
                asm=('@R3'+'\n'+   # base address of two pointers.
                'D=A'+'\n'+
                '@'+index+'\n'+
                'A=D+A'+'\n'+
                'D=M'+'\n'+
                '@SP'+'\n'+    ## push back to stack
                'A=M'+'\n'+
                'M=D'+'\n'+
                '@SP'+'\n'+
                'M=M+1'+'\n')
                
#==============================================================================
#             elif segment == 'static':
#                 asm=('@R16'+'\n'   #base address of static memory
#                 'D=A'+'\n'
#                 '@'+index+'\n'
#                 'A=D+A'+'\n'
#                 'D=M'+'\n'
#                 '@SP'+'\n'
#                 'A=M'+'\n'
#                 'M=D'+'\n'
#                 '@SP'+'\n'
#                 'M=M+1'+'\n')
#==============================================================================
            elif segment == 'static':
                asm = ('@'+self.root+'.'+index+'\n'+
                'D=M'+'\n'+
                '@SP'+'\n'+
                'A=M'+'\n'+
                'M=D'+'\n'+
                '@SP'+'\n'+
                'M=M+1'+'\n')
                
            else:
                asm = 'push '+ segment + ' has not implemented'
                
        elif command == 'pop':
            if segment == 'static':
                asm = ('@SP'+'\n'+
                       'AM=M-1'+'\n'+
                       'D=M'+'\n'+
                       '@'+self.root+'.'+index+'\n'+
                       'M=D'+'\n')
                       
            elif segment == 'this':
                asm=('@THIS'+'\n'+
                'D=M'+'\n'+
                '@'+index+'\n'+
                'D=D+A'+'\n'+
                '@R13'+'\n'+
                'M=D'+'\n'+
                '@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                '@R13'+'\n'+
                'A=M'+'\n'+
                'M=D'+'\n')
                
            elif segment == 'that':
                asm=('@THAT'+'\n'+
                'D=M'+'\n'+
                '@'+index+'\n'+
                'D=D+A'+'\n'+
                '@R13'+'\n'+
                'M=D'+'\n'+
                '@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                '@R13'+'\n'+
                'A=M'+'\n'+
                'M=D'+'\n')
            
            elif segment == 'argument':
                asm=('@ARG'+'\n'
                    'D=M'+'\n'
                    '@'+index+'\n'
                    'D=D+A'+'\n'
                    '@R13'+'\n'
                    'M=D'+'\n'
                    '@SP'+'\n'
                    'AM=M-1'+'\n'
                    'D=M'+'\n'
                    '@R13'+'\n'
                    'A=M'+'\n'
                    'M=D'+'\n')
                
            elif segment == 'local':
                asm=('@LCL'+'\n'+
                    'D=M'+'\n'+
                    '@'+index+'\n'+
                    'D=D+A'+'\n'+
                    '@R13'+'\n'+
                    'M=D'+'\n'+
                    '@SP'+'\n'+
                    'AM=M-1'+'\n'+
                    'D=M'+'\n'+
                    '@R13'+'\n'+
                    'A=M'+'\n'+
                    'M=D'+'\n')
                
            elif segment == 'pointer':
                asm=('@R3'+'\n'+
                    'D=A'+'\n'+
                    '@'+index+'\n'+
                    'D=D+A'+'\n'+
                    '@R13'+'\n'+
                    'M=D'+'\n'+
                    '@SP'+'\n'+
                    'AM=M-1'+'\n'+
                    'D=M'+'\n'+
                    '@R13'+'\n'+
                    'A=M'+'\n'+
                    'M=D'+'\n')
                
            elif segment == 'temp':
                asm=('@R5'+'\n'+
                    'D=A'+'\n'+
                    '@'+index+'\n'+
                    'D=D+A'+'\n'+
                    '@R13'+'\n'+
                    'M=D'+'\n'+
                    '@SP'+'\n'+
                    'AM=M-1'+'\n'+
                    'D=M'+'\n'+
                    '@R13'+'\n'+
                    'A=M'+'\n'+
                    'M=D'+'\n')
            else:
                asm = segment + 'cant pop\n'
        self.outfile.write('//'+command+segment+index+'\n'+asm)
    def write_error(self):
        self.outfile.write('command not recognized')

    def translate_all(self,parser):
        while parser.hasMoreCommands():
            #print parser.hasMoreCommands()
            parser.advance()
            c_type = parser.commandType()
#                    print c_type
            if c_type == 'push' or c_type == 'pop':
                self.write_push_pop(c_type,parser.arg1(),parser.arg2())                
            elif c_type == 'math':
                self.write_arithmetric(parser.command[0])
            elif c_type == 'label':
                self.write_label(parser.arg1())
            elif c_type == 'goto':
                self.write_goto(parser.arg1())
            elif c_type == 'if':
                self.write_if(parser.arg1())
            elif c_type == 'call':
                self.write_call(parser.arg1(),parser.arg2())
            elif c_type == 'return':
                self.write_return()
            elif c_type == 'function':
                self.write_function(parser.arg1(),parser.arg2())
            
            else:
                self.write_error()
        self.writer_close()        
             
        
def main():
#    root = os.getcwd()  
    label_counter = 0
    for (dirpath, dirnames, filenames) in os.walk('./'):
        for a_file in filenames:
            if a_file.endswith('Sys.vm'):     
                vm_file_path = os.path.join(dirpath,a_file).replace('\\','/')
                parser = Parser(vm_file_path)
                
                asm_file_path = os.path.join(dirpath,dirpath.split('\\')[-1]).replace('\\','/') + '.asm'
#                print asm_file_path 
                if os.path.isfile(asm_file_path):   
                    os.remove(asm_file_path)       
                    
                writer = CodeWriter(asm_file_path,label_counter,vm_file_path)
#                print vm_file_path,asm_file_path
                writer.write_init()
                writer.translate_all(parser)
                label_counter = writer.get_label_counter()  
            
            elif  a_file.endswith('.vm'):
                asm_file_path = os.path.join(dirpath,dirpath.split('\\')[-1]).replace('\\','/') + '.asm'    
                if os.path.isfile(asm_file_path):
                    os.remove(asm_file_path)
#                    print os.path.isfile(asm_file_path)

#==============================================================================
#             if a_file.endswith('Sys.vm'):
#                 vm_file_path = os.path.join(dirpath,a_file)
#                 parser = Parser(vm_file_path)
#                 asm_file_path = os.path.join(dirpath,dirpath.split('\\')[-1]) + '.asm'               
#                 writer = CodeWriter(asm_file_path,label_counter)
#                 writer.write_init()
#==============================================================================
    for (dirpath, dirnames, filenames) in os.walk('./'):
        for a_file in filenames:
            if not(a_file.endswith('Sys.vm')) and a_file.endswith('.vm'):                    
                
                vm_file_path = os.path.join(dirpath,a_file).replace('\\','/')
                parser = Parser(vm_file_path)
                asm_file_path = os.path.join(dirpath,dirpath.split('\\')[-1]).replace('\\','/') + '.asm'
#                print asm_file_path           
                writer = CodeWriter(asm_file_path,label_counter,vm_file_path)
#                print vm_file_path,asm_file_path
                writer.translate_all(parser)
                label_counter = writer.get_label_counter()     
                
                
if __name__ == '__main__':
    main()
    
    
    
#==============================================================================
#     
#                 while parser.hasMoreCommands():
#                     #print parser.hasMoreCommands()
#                     parser.advance()
#                     c_type = parser.commandType()
# #                    print c_type
#                     if c_type == 'push' or c_type == 'pop':
#                         writer.write_push_pop(c_type,parser.arg1(),parser.arg2())
#                         
#                     elif c_type == 'math':
#                         writer.write_arithmetric(parser.command[0])
#                     elif c_type == 'label':
#                         writer.write_label(parser.arg1())
#                     elif c_type == 'goto':
#                         writer.write_goto(parser.arg1())
#                     elif c_type == 'if':
#                         writer.write_if(parser.arg1())
#                     elif c_type == 'call':
#                         writer.write_call(parser.arg1(),parser.arg2())
#                     elif c_type == 'return':
#                         writer.write_return()
#                     elif c_type == 'function':
#                         writer.write_function(parser.arg1(),parser.arg2())
#                     
#                     else:
#                         writer.write_error()
#                 writer.writer_close()  
#==============================================================================
