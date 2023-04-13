.data

hello: .asciiz "Hello World!\n"


.text
main:
    # make mistakes to test error messages
    # j foo
    # li $t11, 12

foobar:
    li $t0, 0

exit:
    li $v0, 10
    syscall