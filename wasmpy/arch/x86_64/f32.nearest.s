.globl _start
_start:
flds (%rsp)
sub $2, %rsp
fstcw (%rsp)
mov (%rsp), %ax
and $0b11110011, %ah
push %ax
fldcw (%rsp)
frndint
fldcw 2(%rsp)
add $4, %rsp
fstps (%rsp)
