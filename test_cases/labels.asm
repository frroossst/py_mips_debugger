.text

main:
    li $t0, 80
    j exit

foo:
    li $t1, 80
    j exit

bar:
    li $t2, 80
    j exit

baz:
    li $t3, 80
    j exit

exit:
    li $v0, 10
    syscall