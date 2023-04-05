from helper_instructions import EndOfInstruction
from exceptions import InterpreterSyntaxError, InterpreterRegisterError
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
        elif ins == "sw":
            Instructions.sw(r, m, args[0].strip(","), args[1].strip(","))
        elif ins == "lw":
            Instructions.lw(r, m, args[0].strip(","), args[1].strip(","))
        elif ins == "EndOfInstruction" or ins in ["j", "ja", "jal"]:
            pass
        else:
            raise InterpreterSyntaxError("Invalid instruction: " + ins)

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
        if ins == "ja" or ins == "jal": 
            r.ra = args[0]
        elif ins == "j":
            r.ra = args[0] # this might need to change later on
            
        return None

    def is_a_branch_instruction(ins):
        branch_instructions = ["beq", "bne", "bgt", "blt", "bge", "ble", "beqz", "bnez", "bgtz", "bltz", "bgez", "blez"]
        if ins in branch_instructions:
            return True
        return False

    def check_and_evaluate_branch(r, ins, args):
        try:
            r0 = r.get_register(args[0].lstrip('$'))
            r1 = r.get_register(args[1].lstrip('$'))
        except IndexError:
            pass
        except InterpreterRegisterError:
            pass

        if ins == "beq":
            if r0 == r1:
                return True
        elif ins == "beqz":
            if r0 == 0:
                return True
        elif ins == "bne":
            if r0 != r1:
                return True
        elif ins == "bnez":
            if r0 != 0:
                return True
        elif ins == "bgt":
            if r0 > r1:
                return True
        elif ins == "bgtz":
            if r0 > 0:
                return True
        elif ins == "blt":
            if r0 < r1:
                return True
        elif ins == "bltz":
            if r0 < 0:
                return True
        elif ins == "bge":
            if r0 >= r1:
                return True
        elif ins == "bgez":
            if r0 >= 0:
                return True
        elif ins == "ble":
            if r0 <= r1:
                return True
        elif ins == "blez":
            if r0 <= 0:
                return True

        return False

