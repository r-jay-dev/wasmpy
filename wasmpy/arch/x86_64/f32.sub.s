.globl _start
_start:
flds (%rsp)
addq $4, %rsp
fsubrs (%rsp)
fstps (%rsp)
