.data

hello: .asciiz "Hello World!\n"


.text
main:
    # make mistakes to test error messages
    # j foo
    # li $t11, 12
    # blt $t0, $b1, foobar
    # subui $t0, $t0, 1

foobar:
    li $t0, 0

exit:
    li $v0, 10
    syscall