.data


.text

main:
    # read an int
    li $v0, 5
    syscall

    # store it in $t0
    move $t0, $v0

    # print int
    move $a0, $t0
    li $v0, 1
    syscall
