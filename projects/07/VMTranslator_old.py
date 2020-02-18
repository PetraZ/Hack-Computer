
import sys
import os
#a=file.read()
## intialize varibles
label_eq=0
label_gr=0
label_lt=0

#==============================================================================
# class Parse():
#     def __init__(self,source):
#         a_file = open(source)
#         
#     def has_more_commands(self):
#         
#     def get_command_type(self,line):
#         
#==============================================================================



def get_command_type(line):
    line3=line[0:3]
    if line3=='':
        return ''
    elif line3=='pus':
        return 'PUSH'
    elif line3=='pop':
        return 'POP'
    else:
        return 'ARITHMETIC'

def get_argument(line):
    t=get_command_type(line)
    if t=='PUSH' or t=='POP':
        return line.split()[1:3]
    elif t=='ARITHMETIC':
        return [line]




def translate_command(arg,c_type):
    global label_eq,label_gr,label_lt
    asm=''
    if c_type=='ARITHMETIC':
        if arg[0] =='add':  
            asm=('@SP'+'\n'+         
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'M=M+D'+'\n')
                
        elif arg[0]=='neg':
            asm=('@SP'+'\n'+
                'A=M-1'+'\n'+
                'M=-M'+'\n')
                
        elif arg[0]=='or':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'M=D|M')
                
        elif arg[0]=='sub':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'M=M-D')
            
        elif arg[0]=='and':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'M=M&D')
                
        elif arg[0]=='not':
            asm=('@SP'+'\n'+
                'A=M-1'+'\n'+
                'M=!M')

        elif arg[0]=='eq':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'D=M-D'+'\n'+
                '@EQ'+str(label_eq)+'\n'+
                'D;JEQ'+'\n'+
                '@SP'+'\n'+  
                'A=M-1'+'\n'
                'M=0'+'\n'+
                '@EQEND'+str(label_eq)+'\n'+
                '0;JMP'+'\n'+
                '(EQ'+str(label_eq)+')'+'\n'+
                '@SP'+'\n'+
                'A=M-1'+'\n'+
                'M=-1'+'\n'
                '(EQEND'+str(label_eq)+')')
            label_eq+=1
            
        elif arg[0] =='gt':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'D=M-D'+'\n'+
                '@GR'+str(label_gr)+'\n'+
                'D;JGT'+'\n'+
                '@SP'+'\n'+
                'A=M-1'+'\n'
                'M=0'+'\n'+
                '@GREND'+str(label_gr)+'\n'+
                '0;JMP'+'\n'+
                '(GR'+str(label_gr)+')'+'\n'+
                '@SP'+'\n'+
                'A=M-1'+'\n'+
                'M=-1'+'\n'
                '(GREND'+str(label_gr)+')')
            label_gr+=1
            
        elif arg[0] =='lt':
            asm=('@SP'+'\n'+
                'AM=M-1'+'\n'+
                'D=M'+'\n'+
                'A=A-1'+'\n'+
                'D=M-D'+'\n'+
                '@LT'+str(label_lt)+'\n'+
                'D;JLT'+'\n'+
                '@SP'+'\n'+
                'A=M-1'+'\n'
                'M=0'+'\n'+
                '@LTEND'+str(label_lt)+'\n'+
                '0;JMP'+'\n'+
                '(LT'+str(label_lt)+')'+'\n'+
                '@SP'+'\n'+
                'A=M-1'+'\n'+
                'M=-1'+'\n'
                '(LTEND'+str(label_lt)+')')
            label_lt+=1
            
    elif c_type=='PUSH':
        if arg[0]=='constant':
            asm= ('@'+str(arg[1])+'\n'
                 'D=A'+'\n'
                 '@SP'+'\n'
                 'A=M'+'\n'
                 'M=D'+'\n'
                 '@SP'+'\n'
                 'M=M+1')

        elif arg[0]=='local':
            asm=('@LCL'+'\n'
                'D=M'+'\n'
                '@'+str(arg[1])+'\n'
                'A=D+A'+'\n'
                'D=M'+'\n'
                '@SP'+'\n'
                'A=M'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'M=M+1')


        elif arg[0]=='argument':
            asm=('@ARG'+'\n'
                'D=M'+'\n'
                '@'+str(arg[1])+'\n'
                'A=D+A'+'\n'
                'D=M'+'\n'
                '@SP'+'\n'
                'A=M'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'M=M+1')
                
        elif arg[0]=='this':
            asm=('@THIS'+'\n'
                'D=M'+'\n'
                '@'+str(arg[1])+'\n'
                'A=D+A'+'\n'
                'D=M'+'\n'
                '@SP'+'\n'
                'A=M'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'M=M+1')
                
        elif arg[0]=='that':
            asm=('@THAT'+'\n'
                'D=M'+'\n'
                '@'+str(arg[1])+'\n'
                'A=D+A'+'\n'
                'D=M'+'\n'
                '@SP'+'\n'
                'A=M'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'M=M+1')
                
        elif arg[0]=='temp':
            asm=('@R5'+'\n'
                'D=A'+'\n'
                '@'+str(arg[1])+'\n'
                'A=D+A'+'\n'
                'D=M'+'\n'
                '@SP'+'\n'
                'A=M'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'M=M+1')
                
        elif arg[0]=='pointer':
            asm=('@R3'+'\n'
                'D=A'+'\n'
                '@'+str(arg[1])+'\n'
                'A=D+A'+'\n'
                'D=M'+'\n'
                '@SP'+'\n'
                'A=M'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'M=M+1')
                
        elif arg[0]=='static':
            asm=('@R16'+'\n'
                'D=A'+'\n'
                '@'+str(arg[1])+'\n'
                'A=D+A'+'\n'
                'D=M'+'\n'
                '@SP'+'\n'
                'A=M'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'M=M+1')

    elif c_type=='POP':
#        if arg[0]=='constant':
#            asm=('@SP'+'\n'
#                'M=M-1')
        if arg[0]=='local':
            asm=('@LCL'+'\n'
                'D=M'+'\n'
                '@'+str(arg[1])+'\n'
                'D=D+A'+'\n'
                '@R13'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'AM=M-1'+'\n'
                'D=M'+'\n'
                '@R13'+'\n'
                'A=M'+'\n'
                'M=D')
                
        elif arg[0]=='argument':
            asm=('@ARG'+'\n'
                'D=M'+'\n'
                '@'+str(arg[1])+'\n'
                'D=D+A'+'\n'
                '@R13'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'AM=M-1'+'\n'
                'D=M'+'\n'
                '@R13'+'\n'
                'A=M'+'\n'
                'M=D')
            
        elif arg[0]=='this':
            asm=('@THIS'+'\n'
                'D=M'+'\n'
                '@'+str(arg[1])+'\n'
                'D=D+A'+'\n'
                '@R13'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'AM=M-1'+'\n'
                'D=M'+'\n'
                '@R13'+'\n'
                'A=M'+'\n'
                'M=D')

        elif arg[0]=='that':
            asm=('@THAT'+'\n'
                'D=M'+'\n'
                '@'+str(arg[1])+'\n'
                'D=D+A'+'\n'
                '@R13'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'AM=M-1'+'\n'
                'D=M'+'\n'
                '@R13'+'\n'
                'A=M'+'\n'
                'M=D')
                
        elif arg[0]=='temp':
            asm=('@R5'+'\n'
                'D=A'+'\n'
                '@'+str(arg[1])+'\n'
                'D=D+A'+'\n'
                '@R13'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'AM=M-1'+'\n'
                'D=M'+'\n'
                '@R13'+'\n'
                'A=M'+'\n'
                'M=D')
                
        elif arg[0]=='pointer':
            asm=('@R3'+'\n'
                'D=A'+'\n'
                '@'+str(arg[1])+'\n'
                'D=D+A'+'\n'
                '@R13'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'AM=M-1'+'\n'
                'D=M'+'\n'
                '@R13'+'\n'
                'A=M'+'\n'
                'M=D')
                
        elif arg[0]=='static':
            asm=('@R16'+'\n'
                'D=A'+'\n'
                '@'+str(arg[1])+'\n'
                'D=D+A'+'\n'
                '@R13'+'\n'
                'M=D'+'\n'
                '@SP'+'\n'
                'AM=M-1'+'\n'
                'D=M'+'\n'
                '@R13'+'\n'
                'A=M'+'\n'
                'M=D')

    return asm

def main():
    root = os.getcwd()
    n = 0
    vm_files_lst = []
    for root, dirs, files in os.walk('./'):
        for name in files:
            if(name.endswith(".vm")):
                n += 1
                new_vm_file =  os.path.join(root, name)
                vm_files_lst.append(new_vm_file)
                
                a_file =open(new_vm_file)
                outfile = open(new_vm_file[:-3]+ ".asm", "w")   
                for line in a_file:
                    line=line.rstrip()
                    if line.startswith('//'):
                        continue
                    c_type=get_command_type(line)
                    arg=get_argument(line)
                    trans=translate_command(arg,c_type)
                    outfile.write(trans + "\n")
        #if line.startswith('pop'):
            
                outfile.close()     

if __name__ == "__main__":
    main()

                
                
