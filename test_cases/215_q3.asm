# (10 marks) Write, and test using spim, an assembly language program that inputs two
# character strings from the user, each with at most 20 characters, and then outputs the
# number of unique characters that are found in both strings (don’t count the newline
# character or the zero terminator). For example, with the input strings “monday
# morning” and “coffee spills”, your program should output 3 (for the blank character,
# “o”, and “i”). (Note: an efficient solution is not required, your program can use any
# algorithm that works.)
# There are a number of possible algorithms. This code uses a
# simple (but inefficient) approach. Characters from the
# first string are considered one by one. For each such character,
# the first string is scanned to see if that character has already
# appeared earlier in the string. Only if not, is the second string
# scanned for the character, and a count incremented if it is found.
# The newline character is not considered to be part of the string.

.data

prmpt: .asciiz "Enter two strings (each on separate line and at most 20 characters)\n"
output: .asciiz " unique characters are found in both strings\n"
str1: .space 21
str2: .space 21
newln: .ascii "\n"

.text
# use $s0 ($s1) for the starting address of the first (second) string
# use $s2 ($s3) as a pointer into the first (second) string
# use $s4 ($s5) to hold characters from the first (second) string
# use $s6 for the count
# use $s7 to store the newline character
# use $t0 as an additional pointer into the first string
# use $t2 to hold a previously read character from the first string
main: 
    move $s6,$zero # initializations
    la $s0,str1
    la $s1,str2
    lbu $s7,newln
    li $v0,4 # prompt for, and read, the two strings
    la $a0,prmpt
    syscall
    li $v0,8
    move $a0,$s0
    li $a1,21
    syscall
    li $v0,8
    move $a0,$s1
    li $a1,21
    syscall
    move $s2,$s0

mainlp: 
    lbu $s4,0($s2) # consider characters from 1st string one-by-one
    addiu $s2,$s2,1
    beq $s4,$s7,mainlp # ignore the newline character
    beqz $s4,done # done when hit the null byte
    move $t0,$s0

prevlp: 
    addiu $t0,$t0,1 # check if char occurs previously in 1st string
    ble $s2,$t0,second # if not, check if occurs in 2nd string
    lbu $t2,-1($t0)
    beq $t2,$s4,mainlp # if yes, go on to the next char from 1st string
    j prevlp

second: 
    move $s3,$s1

seclp: 
    lbu $s5,0($s3)
    beqz $s5,mainlp # if doesn't occur in 2nd string, go on to next
    addiu $s3,$s3,1 # char from 1st string
    bne $s5,$s4,seclp
    addiu $s6,$s6,1 # if does occur in 2nd string, increment counter
    j mainlp # and go on to next char from 1st string

done: 
    li $v0,1 # output count and terminate
    move $a0,$s6
    syscall
    li $v0,4
    la $a0,output
    syscall
    li $v0, 10
    syscall