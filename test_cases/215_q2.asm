# (10 marks) Write, and test using spim, an assembly language program that accepts as
# input a sequence of 10 integers. These numbers should be stored in an array in memory,
# in the order in which they were input. Next, your program should prompt the user for an
# integer i. If this integer is between 1 and 10, your program should output the i’th integer
# in the array, and then prompt the user for another integer i. Your program should
# terminate when the integer input by the user is outside the range of 1 to 10.

.data
array: .space 40
prmpt: .asciiz "Enter 10 integers\n"
prmpt2: .asciiz "Enter an integer i\n"
output: .asciiz "The i'th integer is: "
newln: .asciiz "\n"

.text
# use $s1 for the integer i
# use $s2 as an array pointer
# use $s3 as a counter for reading integers
main: 
    li $s3,10 # initialize count
    la $s2,array # initialize array pointer
    li $v0,4 # prompt for entering the 10 integers
    la $a0,prmpt
    syscall

    j readarr

readarr: 
    li $v0,5 # read each integer and store into array
    syscall
    sw $v0,0($s2)
    addi $s2,$s2,4 # advance array pointer
    addi $s3,$s3,-1 # decrement number of integers left to read
    bnez $s3,readarr # repeat if still some left
    la $s2,array # restore $s2 to point to beginning of array

    j loop

loop: 
    li $v0,4 # prompt for integer i
    la $a0,prmpt2
    syscall
    li $v0,5 # read integer i
    syscall
    move $s1,$v0
    blt $s1,1,done # if outside range, quit
    bgt $s1,10,done
    addi $s1,$s1,-1 # transform the integer into array pointer
    sll $s1,$s1,2
    add $s1,$s1,$s2
    li $v0,4 # output
    la $a0,output
    syscall
    li $v0,1
    lw $a0,0($s1)
    syscall
    li $v0,4
    la $a0,newln
    syscall
    j loop

done:   
    li $v0,10
    syscall