.text

main:
    li $t0, 0x400 # 1024

    move $a0, $t0
    li $v0, 1
    syscall

    li $t1, 0b010000000000
    move $a0, $t1
    li $v0, 1
    syscall