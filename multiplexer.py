from helper_instructions import EndOfInstruction
from instructions import Instructions

class Multiplexer:

    def decode_and_execute(r, m, s, ins, args):
        if ins == "li":
            Instructions.li(r, args[0].strip(","), args[1])
        elif ins == "la":
            Instructions.la(r, m, args[0].strip(","), args[1])
        elif ins == "move":
            Instructions.move(r, args[0].strip(","), args[1].strip(","))
        elif ins == "addi":
            Instructions.addi(r, args[0].strip(","), args[1].strip(","), args[2])
        elif ins == "syscall":
            Instructions.process_syscall(r, m, s)

    def reached_end_of_instruction(ins):
        if ins == EndOfInstruction().__str__():
            return True
        return False

    # expand to include more jumps
    def is_a_jump_instruction(ins):
        if ins == "j" or ins == "ja" or ins == "jal":
            return True
        return False

    def process_jump_instruction(r, ins, args):
        if ins == "ja":
            r.ra = args[0]
        elif ins == "jal":
            # check if label or address
            r.ra = args[0]
        elif ins == "j":
            r.ra = args[0]
            
        return None

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
        elif ins == "ble" and args[0] <= args[1]:
                return True
        return False

