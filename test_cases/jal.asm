.text

# commenting out all load adresses into $ra reads to a 
# ISORL: Interpreter Stack Overflow Recursion Limit, 
# because the same address is loaded into $ra multiple 
# times and the label keep recursively executing itself
# on loading the address into $ra, the address works as 
# expected and the program terminates gracefully

main:
    jal foo
    li $t5, 99

foo:
    li $t0, 20
    jal bar
    li $ra, 40004
    jr $ra

bar:
    li $t1, 30
    li $ra, 40016
    jr $ra