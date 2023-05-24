# (10 marks) Write a MIPS procedure that takes as its three parameters the address of a
# zero-terminated string, a character c, and an integer n, and returns the number of distinct
# runs of consecutive instances of c in the string that are of length at least n. Also, write a
# simple main program to test your procedure. Your main program should input a string
# from the user (you may assume that the string has at most 20 characters), input the
# character and the integer, invoke your procedure, output the return value, and then
# terminate. For example, given the inputs “bbabbbbagbgbb”, “b”, and 2, the output should
# be 3. Your code must use the “standard” conventions covered in class for passing
# parameters and returning results.

.data
    prmpt: .asciiz "Enter a string of at most 20 characters\n"
    prmpt2: .asciiz "Enter a character\n"
    prmpt3: .asciiz "\nEnter the minimum length of run\n"
    output: .asciiz "Number of qualifying runs is "
    newln: .asciiz "\n"
    str: .space 22

.text
# use $s0 for the input character, and to store procedure call return value
# procedure arguments as follows:
# $a0 - address of string
# $a1 - the character c
# $a2 - the integer n
main:   
    li $v0,4
    la $a0,prmpt
    syscall
    li $v0,8
    la $a0,str
    li $a1,22
    syscall
    li $v0,4
    la $a0,prmpt2
    syscall
    li $v0,12
    syscall
    move $s0,$v0
    li $v0,4
    la $a0,prmpt3
    syscall
    li $v0,5
    syscall
    la $a0,str
    move $a1,$s0
    move $a2,$v0
    jal count
    move $s0,$v0
    li $v0,4
    la $a0,output
    syscall
    li $v0,1
    move $a0,$s0
    syscall
    li $v0,4
    la $a0,newln
    syscall
    li $v0,10
    syscall

count:  
    move $v0,$zero
    loop: lbu $t0,0($a0)
    beq $t0,$zero,done
    addi $a0,$a0,1
    bne $t0,$a1,loop
    move $t1,$zero

loop2: 
    addi $t1,$t1,1
    lbu $t0,0($a0)
    addi $a0,$a0,1
    beq $t0,$a1,loop2
    blt $t1,$a2,nope
    addi $v0,$v0,1

nope: 
    bne $t0,$zero,loop

done: 
    jr $ra