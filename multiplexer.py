from instructions import Instuctions

class Multiplexer:

    def decode_and_execute(r, ins, args):
        if ins == "li":
            Instuctions.li(r, args[0].strip(","), args[1])
        elif ins == "addi":
            Instuctions.addi(r, args[0].strip(","), args[1])

    # expand to include more jumps
    def is_a_jump_instruction(ins):
        if ins == "j":
            return True
        return False