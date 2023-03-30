# (10 marks) One of the lesser-known mathematical functions is what we will call here the
# CS215 function. This is a function of three nonnegative integer variables i, j, and k, that
# can be defined recursively as follows:
# CS215(0, 0, 0) = 1
# CS215(i, j, k) = CS215(⌊𝑘+1
# 2 ⌋ , ⌊𝑗
# 2⌋ , ⌊|𝑖−𝑗|
# 2 ⌋) + CS215(⌊𝑖+𝑘
# 2 ⌋ , ⌊𝑘
# 2⌋ , ⌊𝑗+1
# 2 ⌋) + CS215(⌊𝑘
# 4⌋ , ⌊𝑖
# 4⌋ , ⌊𝑗
# 4⌋)+1,
# for all nonnegative integers i, j, k, such that at least one of i, j, k is nonzero.
# Here |𝑛| denotes the absolute value of n, and ⌊ 𝑛
# 𝑚⌋ denotes the integer result when n is
# divided by m, discarding any remainder. Some examples of CS215 function values are as
# follows: CS215 (0, 1, 0) = 10, CS215 (2, 1, 5) = 46, CS215 (20, 10, 50) = 1357, CS215
# (5, 2, 1) = 52, CS215 (10, 50, 20) = 1435, CS215 (215, 215, 215) = 16210.
# Write a recursive MIPS procedure CS215 implementing this function, and a main
# program to test it. Your procedure should take as its three parameters nonnegative integers
# i, j, and k, and should return the function value. Your main program should prompt the
# user to enter three nonnegative integers i, j, and k. If at least one of the entered integers is
# negative, your program should terminate. Otherwise, your program should call your
# CS215 procedure, print the returned result, and then repeat by again prompting the user to
# enter three nonnegative integers. Your code must use the “standard” conventions
# covered in class for passing parameters and returning results.

.data
    prompt: .asciiz "Enter three nonnegative integers i, j, and k:\n"
    outmsg: .asciiz "The function value is: "
    newl: .asciiz "\n"

.text
# The main program tests a recursive implementation of the CS215
# function. The user is prompted to enter three nonnegative integers.
# If at least one of these integers is negative, the program terminates.
# Otherwise, CS215 is invoked, and the return result is printed.
# The program then repeats, asking the user to again enter three
# nonnegative integers.
main: 
    li $v0,4
    la $a0,prompt
    syscall
    li $v0,5
    syscall # read i
    move $s0,$v0
    li $v0,5
    syscall # read j
    move $s1,$v0
    li $v0,5
    syscall # read k
    bltz $s0,done
    bltz $s1,done
    bltz $v0,done # quit if any are negative
    move $a2,$v0
    move $a1,$s1
    move $a0,$s0
    jal CS215
    move $s0,$v0
    li $v0,4
    la $a0,outmsg
    syscall
    li $v0,1
    move $a0,$s0
    syscall # output CS215 (i, j, k)
    li $v0,4
    la $a0,newl
    syscall
    j main # go back and repeat

done:   
    li $v0,10
    syscall

# procedure CS215 is a recursive implementation of the CS215 function
# procedure parameters are as follows (all assumed to be nonnegative):
# $a0 - first function parameter (i)
# $a1 - second function parameter (j)
# $a2 - third function parameter (k)
CS215:  
    bgtz $a0,notbs
    bgtz $a1,notbs
    bgtz $a2,notbs
    li $v0,1 # base case, value is 1
    jr $ra

notbs: 
    addiu $sp,$sp,-20 # add space to stack for return address, arguments,
    # and result from first recursive call
    sw $ra,16($sp) # save return address, arguments on stack
    sw $a0,12($sp)
    sw $a1,8($sp)
    sw $a2,4($sp)
    srl $t0,$a1,1 # calculate arguments for first recursive call
    sub $t1,$a0,$a1
    abs $t1,$t1
    srl $t1,$t1,1
    addi $a2,$a2,1
    srl $a2,$a2,1
    move $a0,$a2 # move into argument registers
    move $a1,$t0
    move $a2,$t1
    jal CS215 # make first recursive call
    sw $v0,0($sp) # save result from recursive call on stack
    lw $a2,4($sp) # restore saved arguments from stack
    lw $a1,8($sp)
    lw $a0,12($sp)
    add $t0,$a0,$a2 # calculate arguments for second recursive call
    srl $t0,$t0,1
    srl $t1,$a2,1
    addi $a1,$a1,1
    srl $a1,$a1,1
    move $a2,$a1 # move into argument registers
    move $a0,$t0
    move $a1,$t1
    jal CS215 # make second recursive call
    lw $t0,0($sp) # restore result from first recursive call
    add $t0,$v0,$t0 # sum results from first and second calls
    sw $t0,0($sp) # store back on stack
    lw $a2,4($sp) # restore saved arguments from stack
    lw $a1,8($sp)
    lw $a0,12($sp)
    srl $t0,$a2,2 # calculate arguments for third recursive call
    srl $a2,$a1,2
    srl $a1,$a0,2
    move $a0,$t0
    jal CS215 # make third recursive call
    lw $t0,0($sp) # restore sum from first and second calls
    add $v0,$v0,$t0 # calculate result
    addi $v0,$v0,1
    lw $ra,16($sp) # restore return address
    addi $sp,$sp,20 # remove space added to stack
    jr $ra