.globl _start
_start:
popl %eax
popl %ecx
popcnt %eax, %eax
popcnt %ecx, %ecx
add %ecx, %eax
pushl $0
pushl %eax
