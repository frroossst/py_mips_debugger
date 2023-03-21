.data

.text

foo:
    addi $t0, $t0, 1
    addi $t1, $t1, 1
    addi $t2, $t2, 1
    addi $t3, $t3, 1
    addi $t4, $t4, 1

bar:
    addi $t5, $t5, 1
    addi $t6, $t6, 1
    addi $t7, $t7, 1
    addi $t8, $t8, 1
    addi $t9, $t9, 1

main:
    li $t0, 0
    li $t1, 1
    li $t2, 2
    li $t3, 3
    li $t4, 4
    li $t5, 5
    li $t6, 6
    li $t7, 7
    li $t8, 8
    li $t9, 9

    jal foo
    jal bar

    addi $t0, $t0, 1
    addi $t3, $t3, 1
    addi $t5, $t5, 1
    addi $t7, $t7, 1
    addi $t9, $t9, 1