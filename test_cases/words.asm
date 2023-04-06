.data

foo: .word 0
bar: .word 1

.text

main:
    li $t0, 128
    sw $t0, foo

    lw $t1, foo

    # print $t0
    move $a0, $t1
    li $v0, 1
    syscall

    # testing offsets
    la $t2, foo
    lw $t3, 0($t2)

    # exit
    li $v0, 10
    syscall
