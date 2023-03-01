# work on this after implementing memory address mapping

.data

.text

a:
    li $t1, 9
    la $t3, b
    ja $t3

b:
    li $t2, 10

main:
    li $t0, 1
    j a
