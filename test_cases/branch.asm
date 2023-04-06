.data
helloworld: .asciiz "Hello World!\n"

.text
foo:
    li $v0, 4
    la $a0, helloworld
    syscall

    # exit
    li $v0, 10
    syscall

bar:
    li $t2, 125

main:
    li $t0, 1
	# li $t1, 2
    # bgt $t0, $t1, foo
	bgt $t0, $zero, foo
