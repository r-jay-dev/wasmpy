.globl _start
_start:
flds (%esp)
pop %eax
fadds (%esp)
fstps (%esp)
