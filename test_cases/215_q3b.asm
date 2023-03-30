# MIPS assembly function to calculate distinct runs of a character in a string

#######################################################################
#                             Index                                   #
#######################################################################
# $s0 => 
# $s1 => character read from user
# $s2 => integer read from user


    .data

prompt0: .asciiz "Enter a string: "
prompt1: .asciiz "Enter a character: "
prompt2: .asciiz "Enter a number: "
endl: .asciiz "\n"
debug: .asciiz "here"
result: .asciiz "Distinct runs: "

strin: .space 21

    .text

exit:
    # print $t3 as int
    li $v0, 1
    move $a0, $t3
    syscall

    li $v0, 10
    syscall

main:
    # print prompt0
    li $v0, 4
    la $a0, prompt0
    syscall

    # read string
    li $v0, 8
    la $a0, strin
    li $a1, 20
    syscall

    # print endl
    li $v0, 4
    la $a0, endl
    syscall

    # print prompt1
    li $v0, 4
    la $a0, prompt1
    syscall

    # read character
    li $v0, 12
    syscall
    move $s1, $v0

    # print endl
    li $v0, 4
    la $a0, endl
    syscall

    # print prompt2
    li $v0, 4
    la $a0, prompt2
    syscall

    # read number
    li $v0, 5
    syscall
    move $s2, $v0

    # print endl
    li $v0, 4
    la $a0, endl
    syscall

    # pass as args to a funtion
    li $t0, 0
    la $t1, strin
    li $t3, 0 # count of consecutive char in string
    jal countRecurring

    j exit

incrementCount:
    addi $t3, $t3, 1
    j countRecurring

sameCharDetected:
    # consume similar characters while keeping a count
    addi $s3, $s3, 1
    addi $t1, $t1, 1
    lbu $t2, 0($t1)

    beq $t2, $zero, exit # not the end of the string
    beq $t2, $s1, sameCharDetected

    # print $s3
    li $v0, 1
    move $a0, $s3
    syscall

    bge $s3, $s2, incrementCount

countRecurring:
    # loop over string and print character
    lbu $t2, 0($t1)

    beq $t2, $zero, exit # not the end of the string

    # print character
    li $v0, 11
    move $a0, $t2
    syscall

    # check if current character is the same as the one we are looking for
    li $s3, 0
    beq $t2, $s1, sameCharDetected

    addi $t1, $t1, 1 # increment pointer to next character

    j countRecurring