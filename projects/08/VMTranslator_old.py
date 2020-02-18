
import sys
import os
#a=file.read()
## intialize varibles
label_eq=0
label_gr=0
label_lt=0
fun_counter=0
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
    elif line3=='lab':
        return 'LABEL'
    elif line3=='got':
        return 'GOTO'
    elif line3=='if-':
        return 'IF-GOTO'
    elif line3=='fun':
        return 'FUNCTION'
    elif line3=='cal':
        return 'CAll'
    elif line3=='ret':
        return 'RETURN'
    else:
        return 'ARITHMETIC'

def get_argument(line):
    t=get_command_type(line)
    if t=='PUSH' or t=='POP':
        return line.split()[1:3]
    elif t=='LABEL' or  t=='GOTO' or t=='IF-GOTO' :
        return line.split()[1]
    elif t=='FUNCTION' or t=='CALL':
        return line.split()[0:3]
    elif t=='RETURN':
        return ''
    elif t=='ARITHMETIC':
        return [line]




def translate_command(arg,c_type):
    global label_eq,label_gr,label_lt,fun_counter
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
            
    elif c_type=='LABEL':
        asm = '('+str(arg[0])+')'
        
    elif c_type=='GOTO':
        asm = ('@'+str(arg[0])+'\n'
               '0;JMP')
        
    elif c_type=='IF-GOTO':
        asm = ('@SP'+'\n'
               'AM=M-1'+'\n'
               'D=M'+'\n'
               '@'+str(arg[0])+'\n'
               'D;JNE'
               )
    elif c_type=='CALL':
        asm = (
               '@'+str(arg[1])+str(fun_counter)+'\n'   #### store the address of ROM
               'D=A'+'\n' 
               '@SP'+'\n'
               'A=M'+'\n'
               'M=D'+'\n'
               '@SP'+'\n'
               'M=M+1'+'\n'   # push return address
               
               '@LCL'+'\n'
               'D=M'+'\n'
               '@SP'+'\n'
               'A=M'+'\n'
               'M=D'+'\n'   
               '@SP'+'\n'
               'M=M+1'+'\n'    # push LCL address
               
               '@ARG'+'\n'
               'D=M'+'\n'
               '@SP'+'\n'
               'A=M'+'\n'
               'M=D'+'\n'
               '@SP'+'\n'
               'M=M+1'+'\n'  # push ARG 
               
               '@THIS'+'\n'
               'D=M'+'\n'
               '@SP'+'\n'
               'A=M'+'\n'
               'M=D'+'\n'
               '@SP'+'\n'
               'M=M+1'+'\n' # push THIS
               
               '@THAT'+'\n'
               'D=M'+'\n'
               '@SP'+'\n'
               'A=M'+'\n'
               'M=D'+'\n'
               '@SP'+'\n'
               'M=M+1'+'\n'  ## push THAT
               
               '@SP'+'\n'
               'D=M'+'\n'
               '@'+str(arg[2])+'\n'
               'D=D-A'+'\n'
               '@R5'+'\n'
               'D=D-A'+'\n'
               '@ARG'+'\n'
               'M=D'+'\n'  ### REOSITION ARG
               
               '@SP'+'\n'
               'D=M'+'\n'
               '@LCL'+'\n'
               'M=D'+'\n'  ## reposition LCL
               
               '@'+str(arg[1])+'\n'
               '0;JMP'+'\n'
               '('+str(arg[1])+str(fun_counter)+')'  ## a lalbel in ROM since excute a function goes into another module (other places in ROM)
                                                     ## We gotta remember where we have executed in the rom and keep going.
               )
        fun_counter+=1          
               
    elif  c_type=='FUNCTION':
        asm = (
               '('+str(arg[1])+'func_start'+')'+'\n'  ## label function entry
               
               '@'+str(arg[2])+'\n'                   ## How many local variables
               'D=A'+'\n'
               '@'+str(arg[1])+'.klocal'+'\n'         ## store in a variable
               'M=D'+'\n'
               
               '('+str(arg[1])+'loop_start'+')'+'\n'
               
               '@'+str(arg[1])+'.klocal'+'\n'
               'D=M'+'\n'
               '@'+str(arg[1])+'loop_end'+'\n'
               'D;JEQ'+'\n'
               
               '@0'+'\n'
               'D=A'+'\n'
               '@SP'+'\n'
               'A=M'+'\n'
               'M=D'+'\n'
               '@SP'+'\n'
               'M=M+1'+'\n'                           # push 0 into SP(ARG) 
               
               '@'+str(arg[1])+'.klocal'+'\n'
               'M=M-1'+'\n'                           # num_local -= 1
               
               '@'+str(arg[1])+'loop_start'+'\n'
               '0;JMP'+'\n'
               
               '('+str(arg[1])+'loop_end)'
               
               )
    elif c_type=='RETURN':
        asm =(
              '@LCL'+'\n'
              'D=M'+'\n'
              '@R13'+'\n'   ##R13 is  tempera var as FRAME
              'M=D'+'\n'    ## store LCL address in FRAME(@R13)
              
              '@R14'+'\n'
              'M=D'+'\n'     #'LCL' address
              '@R5'+'\n'
              'D=A'+'\n'
              '@R14'+'\n'  ##R14 as a temp var for Return
              'M=M-D'+'\n'
              
              '@SP'+'\n'     ##the function has finished and now the return value
              'A=M-1'+'\n'              ##is at the topmost in the stack SP-1
              'D=M'+'\n'
              '@ARG'+'\n'
              'A=M'+'\n'
              'M=D'+'\n'       ## PUT RETURN VALUE AT ARG POSITION
              
              '@ARG'+'\n'
              'D=M+1'+'\n'
              '@SP'+'\n'
              'M=D'+'\n'   ##SP=ARG+1
              
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
              '0;JMP'
              )
    return asm

    
    
def write_init():
    asm = ('@256' + '\n'+
          'D=A' +'\n'+
          '@SP' +'\n'+
          'M=D' +'\n')
    
    call_init = translate_command('call Sys.init 0','CALL')      
    
    asm = asm + call_init +'\n'
    return asm      
    
    
    
    
def main():
    root = os.getcwd()
    n = 0
    vm_files_lst = []
    previous_asm_file = ''
    for root, dirs, files in os.walk('./'):
        for name in files:
            if(name.endswith(".vm")):
                n += 1
                new_vm_file =  os.path.join(root, name)
                asm_file =  os.path.join(root, root.split('\\')[-1])
                vm_files_lst.append(new_vm_file)
                
                a_file =open(new_vm_file)
                outfile = open(asm_file + ".asm", "w")
                if previous_asm_file != asm_file:
                    outfile.write(write_init())
                    print asm_file
                previous_asm_file = asm_file
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

                
                
