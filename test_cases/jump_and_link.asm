.data

.text
a:
    li $t1, 10

b:
    li $t2, 9

# this is a comment

main:
    li $t0, 1
    jal a
    j b