from instructions import Instructions

class Multiplexer:

    def decode_and_execute(r, ins, args):
        if ins == "li":
            Instructions.li(r, args[0].strip(","), args[1])
        elif ins == "addi":
            Instructions.addi(r, args[0].strip(","), args[1].strip(","), args[2])

    # expand to include more jumps
    def is_a_jump_instruction(ins):
        if ins == "j":
            return True
        return False

    def check_and_evaluate_branch(ins, args):
        if ins == "beq":
            if args[0] == args[1]:
                return True
        elif ins == "bne":
            if args[0] != args[1]:
                return True
        elif ins == "bgt":
            if args[0] > args[1]:
                return True
        elif ins == "blt":
            if args[0] < args[1]:
                return True
        elif ins == "bge":
            if args[0] >= args[1]:
                return True
        elif ins == "ble":
            if args[0] <= args[1]:
                return True
        return False

