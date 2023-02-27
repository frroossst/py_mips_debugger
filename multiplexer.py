from registers import Registers
from instructions import *

class Multiplexer:

    def decode_instruction(r, ins, args):
        if ins == "li":
            li(r, args[0], args[1])




