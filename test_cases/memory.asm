.data

hello: .asciiz "Hello World!\n"

.text

exit:
    li $v0, 10
    syscall

main:
    li $v0, 4
    la $a0, hello
    syscall

    j exit
