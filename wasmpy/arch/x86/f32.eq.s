.globl _start
_start:
popl %eax
popl %ecx
cmpl %eax, %ecx
je true
pushl $0
jmp end
true:
pushl $1
end:
