.text

main:
    jal foo
    li $t5, 99

foo:
    li $t0, 20
    jal bar
    jr $ra

bar:
    li $t1, 30
    jr $ra