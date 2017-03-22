def get_command_type(line):
    line1=line[0:1]
    if line1=='(':
        return 'L'
    elif line1=='@':
        return 'A'
    else:
        return 'C'

def first_pass(fname,outname):
    
    linenumber=0
    global table
    outfile=open(outname,'w')
    infile = open(fname)
    for line in infile :
        sline=strip(line)
        
        if line=='':
            continue
        
    
        elif sline!='':
            
            if sline[0]=='(':
                label=sline[1:-1]
                table[label]=linenumber
                sline=''
            else:
                linenumber=linenumber+1
                outfile.write(sline+'\n')
    infile.close()
    outfile.close()
    
valadd=16
def addvariable(label):
    global valadd,table
    table[label]=valadd
    valadd+=1
    return table[label]

def get_argument(line):
    t=get_command_type(line)
    arg=['','','']
    
    if t == 'A':
        if line[1].isalpha():
            label=line[1:]
            avalue = table.get(label,-1)
            if avalue==-1:
                avalue = addvariable(label)
            
        else:
            avalue = int(line[1:])
        arg[0]=bin(avalue)[2:].zfill(16)
        
    
    elif t == 'C':
        if not( ';' in line):
            arg[0]=line.split('=')[0]      ## dest
            arg[1]=line.split('=')[1]       ## comp
                                         ##  no jump
        elif not ('='in line):
            arg[1]=line.split(';')[0]
            arg[2]=line.split(';')[1]
        else:
            arg[0]=line.split('=')[0]
            arg[1]=(line.split('=')[1]).split(';')[0]
            arg[2]=line.split(';')[1]
    return arg
    
def assembler(c_type,arg):
    if c_type == 'A':
        return arg[0]
    
    elif c_type == 'C':
        if  arg[0]== '':
            d='000'
        elif arg[0]== 'M':
            d='001'
        elif arg[0]== 'D':
            d='010'
        elif arg[0]=='MD':
            d='011'
        elif arg[0]=='A':
            d='100'
        elif arg[0]=='AM':
            d='101'
        elif arg[0]=='AD':
            d='110'
        elif arg[0]=='AMD':
            d='111'
        else:
            print 'No Dest Match'

        if arg[2]=='':
            j='000'
        elif arg[2]=='JGT':
            j='001'
        elif arg[2]=='JEQ':
            j='010'
        elif arg[2]=='JGE':
            j='011'
        elif arg[2]=='JLT':
            j='100'
        elif arg[2]=='JNE':
            j='101'
        elif arg[2]=='JLE':
            j='110'
        elif arg[2]=='JMP':
            j='111'
        else:
            print 'No Jump Match'

        if arg[1]=='0':
            c='0'+'101010'
        elif arg[1]=='1':
            c='0'+'111111'
        elif arg[1]=='-1':
            c='0'+'111010'
        elif arg[1]=='D':
            c='0'+'001100'
        elif arg[1]=='A':
            c='0'+'110000'
        elif arg[1]=='!D':
            c='0'+'0011101'
        elif arg[1]=='!A':
            c='0'+'110011'
        elif arg[1]=='-D':
            c='0'+'001111'
        elif arg[1]=='-A':
            c='0'+'110011'
        elif arg[1]=='D+1':
            c='0'+'011111'
        elif arg[1]=='A+1':
            c='0'+'110111'
        elif arg[1]=='D-1':
            c='0'+'001110'
        elif arg[1]=='A-1':
            c='0'+'110010'
        elif arg[1]=='D+A':
            c='0'+'000010'
        elif arg[1]=='D-A':
            c='0'+'010011'
        elif arg[1]=='A-D':
            c='0'+'000111'
        elif arg[1]=='D&A':
            c='0'+'000000'
        elif arg[1]=='D|A':
            c='0'+'010101'

        elif arg[1]=='M':
            c='1'+'110000'
        elif arg[1]=='!M':
            c='1'+'110001'
        elif arg[1]=='-M':
            c='1'+'110011'
        elif arg[1]=='M+1':
            c='1'+'110111'
        elif arg[1]=='M-1':
            c='1'+'110010'
        elif arg[1]=='D+M':
            c='1'+'000010'
        elif arg[1]=='D-M':
            c='1'+'010011'
        elif arg[1]=='M-D':
            c='1'+'000111'
        elif arg[1]=='D&M':
            c='1'+'000000'
        elif arg[1]=='D|M':
            c='1'+'010101'
        else:
            print 'No Comp Match'
    return ('111'+c+d+j)

#def clean_line (line):
#    if line


table ={
    'SP':0,
    'LCL':1,
    'ARG':2,
    'THIS':3,
    'THAT':4,
    'SCREEN':16384,
    'KBD':24576,
    }
for i in range(0,16):
    label='R'+str(i)
    table[label]=i

    
def strip(line):
# removes whitespace and comments; returns line without a closing \n

    char = line[0]
    if char == "\n" or char == "/":
        return ""
    elif char == " ":
        return strip(line[1:])
    else:
        return char + strip(line[1:])

first_pass('Pong.asm','Pongtmp')    
file=open('Pongtmp')
output=open('Pong.hack','w')
for line in file:
    line= strip(line)
    if line=='':
        continue
    else:
        #print line
        c_type=get_command_type(line)
        
        arg=get_argument(line)
        
        assem=assembler(c_type,arg)
        
        #print assem
        output.write(assem+'\n')

file.close()
output.close()
