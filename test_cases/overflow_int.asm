.data

.text

main:
    # li $t0, 4294967296
    # does not overflow
    li $t0, 2147483647
    # does overflow
    li $t1, 2147483648

    # print li 
    li $v0, 1
    move $a0, $t0
    syscall

    # exit
    li $v0, 10
    syscall
