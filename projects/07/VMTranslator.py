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
                       'if'   : 'if',
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
    def __init__(self,dest):
        self.root = dest[:-4].split('/')[-1]
        self.outfile = open(dest,'w')
        self.label_number = 0
        
    def set_file_name(self,file_name):
        self.file_name = file_name
        
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
#        comment ='//'+command+'\n'
        self.outfile.write(asm)
        
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
#        comment = '//'+command+segment+index+'\n'
        self.outfile.write(asm)
    def write_error(self):
        self.outfile.write('command not recognized\n')
        
def main():
#    root = os.getcwd()  
    for (dirpath, dirnames, filenames) in os.walk('./'):
        for a_file in filenames:
            if a_file.endswith('vm'):
                vm_file_path = os.path.join(dirpath,a_file)
#                print vm_file_path
                parser = Parser(vm_file_path)
                asm_file_path = os.path.join(dirpath,dirpath.split('\\')[-1]) + '.asm'                
                writer = CodeWriter(asm_file_path)
#                print asm_file_path
                while parser.hasMoreCommands():
                    #print parser.hasMoreCommands()
                    parser.advance()
                    c_type = parser.commandType()
#                    print c_type
                    if c_type == 'push' or c_type == 'pop':
                        writer.write_push_pop(c_type,parser.arg1(),parser.arg2())
                        
                    elif c_type == 'math':
                        writer.write_arithmetric(parser.command[0])
                    else:
                        writer.write_error()
        
if __name__ == '__main__':
    main()