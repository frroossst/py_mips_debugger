from instructions import Instructions
from registers import Registers
from memory import Memory

from datatypes_t import *
from exceptions import *

import random



def get_random_value():
    return random.randint(0, 32000)

def get_random_register():
    to_remove = ["$zero", "hi", "lo", "ra"]
    reg_li = Registers().get_all_registers_as_list()
    return random.choice(list(filter(lambda x: x not in to_remove, reg_li)))

def test(result, expected):
    assert result == expected, f"Expected {expected}, got {result}" 


# testing instructions

# test for li
R = Registers()
M = Memory()

for _ in range(10):
    val = get_random_value()
    reg = get_random_register()
    Instructions.li(R, "$" + reg, val)
    result = R.get_register(reg)
    test(result, val)

# test for la


# test for move
R = Registers()
M = Memory()

for _ in range(10):
    val = get_random_value()
    reg0 = get_random_register()
    reg1 = get_random_register()
    Instructions.li(R, "$" + reg0, val)
    Instructions.move(R, "$" + reg1, "$" + reg0)
    reg1 = R.get_register(reg1)
    test(reg0, reg1)
