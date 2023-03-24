.data
prompt: .asciiz "Enter an integer: "

.text

main:
    # print prompt
    la $a0, prompt
    li $v0, 4
    syscall

    # read an int
    li $v0, 5
    syscall

    # store it in $t0
    move $t0, $v0

    # print int
    move $a0, $t0
    li $v0, 1
    syscall
