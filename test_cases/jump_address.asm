# work on this after implementing memory address mapping

.data

str1: .asciiz "Hello World!"
str2: .asciiz "reached here"
str3: .asciiz "reached here 2"

.text

ba:
    li $t2, 10

a:
    li $t1, 9
    la $t3, ba

    # print an
    la $a0, str2
    li $v0, 4
    syscall

    # ja $t3

main:
    li $t0, 1

    # print mn
    la $a0, str1
    li $v0, 4
    syscall

    j a
