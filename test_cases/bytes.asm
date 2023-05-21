.data
myString: .asciiz "Hello, World!"

.text
main:
    la $t0, myString   # load the address of myString into $t0
    lbu $t1, 0($t0)    # load the first byte of myString into $t1

    li $v0, 11         # set the system call code for printing a character
    move $a0, $t1      # move the value to be printed into $a0
    syscall            # make the system call

    li $v0, 10         # set the system call code for exiting the program
    syscall            # make the system call
