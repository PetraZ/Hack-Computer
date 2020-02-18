

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
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

(W)
@W
0;JMP
