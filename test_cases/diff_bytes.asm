.data
    byte1: .byte 128

.text
    main:
        la $t0, byte1
        lbu $t1, 0($t0) # load byte unsigned
        lb $t2, 0($t0)  # load byte

        # print $t1
        move $a0, $t1  # 128
        li $v0, 1
        syscall

        # print $t2
        move $a0, $t2  # -128
        li $v0, 1
        syscall

        li $v0, 10
        syscall
