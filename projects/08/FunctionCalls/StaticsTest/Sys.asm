
(Sys.initfunc_start)
@0
D=A
@Sys.init.klocal
M=D
(Sys.initloop_start)
@Sys.init.klocal
D=M
@Sys.initloop_end
D;JEQ
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@Sys.init.klocal
M=M-1
@Sys.initloop_start
0;JMP
(Sys.initloop_end)
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

@R5
D=A
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
@15
D=A
@SP
A=M
M=D
@SP
M=M+1

@R5
D=A
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D


(W)
@W
0;JMP
