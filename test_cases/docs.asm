.data

.text

# @brief this does things
# @post this does not affect anything
# @note dont use this
# @param $a0 is the first argument
# @param $a1 is the second argument
# @return $v0 is the return value
foo:
    move $v0, $a0
	li $t0, 20

main:
    j foo