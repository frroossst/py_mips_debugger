# (10 marks) Write,  and test using spim,  an assembly language program that prompts the
# user for an integer input,  accepts such an input,  and then repeats,  continuing until the
# input integer is zero. When zero is input,  your program should output the sum of the
# negative integers that were input and the sum of the positive integers that were input, 
# and then terminate.

.data
prmpt: .asciiz "Enter an integer\n"
sumneg: .asciiz "\nThe sum of the negative integers is: "
sumpos: .asciiz "\nThe sum of the positive integers is: "
newln: .asciiz "\n"

.text
# use $s0 for the sum of negative integers
# use $s1 for the sum of positive integers
main: 
    move $s0, $zero #initialize sums
    move $s1, $zero
    j loop

loop: 
    li $v0, 4 # output prompt for entering an integer
    la $a0, prmpt
    syscall
    li $v0, 5 # read integer
    syscall
    bgtz $v0, pos # is it > 0? if so,  add to sum of positive integers
    beqz $v0, done # is it = 0? if so,  can print out sums and terminate
    add $s0, $s0, $v0 # must be negative – add to sum of negative integers
    j loop

pos: 
    add $s1, $s1, $v0
    j loop

done: 
    li $v0, 4 # print sum of negative integers
    la $a0, sumneg
    syscall
    li $v0, 1
    move $a0, $s0
    syscall
    li $v0, 4
    la $a0, newln
    syscall
    li $v0, 4 # print sum of positive integers
    la $a0, sumpos
    syscall
    li $v0, 1
    move $a0, $s1
    syscall
    li $v0, 4
    la $a0, newln
    syscall
    li $v0, 10
    syscall # done