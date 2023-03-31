from exceptions import InterpreterControlFlowError, InterpreterRegisterError, InterpreterSyntaxError

class Instructions:

    @staticmethod
    def sanitise_instruction(r, m, ins):
        rem_com_li = []
        # remove comments till the end of the line
        for x, i in enumerate(ins):
            if i.startswith("#"):
                rem_com_li = ins[:x:]

        # instruction not found
        if rem_com_li[0] not in Instructions.get_all_instructions:
            raise InterpreterSyntaxError(f"invalid instruction: {rem_com_li[0]}")

        # check instruction type and check arg valifity
        j_format = ["j", "jal", "jr"]
        r_format = ["add", "sub"]
        i_format = ["li", "addi", "subi"]
        b_format = ["beq", "bne", "bgt", "blt", "bge", "ble", "bgtz", "bltz", "bgez", "blez"]
        l_format = ["lw", "sw"]

        if rem_com_li[0] in j_format:
            if len(rem_com_li) != 2:
                raise InterpreterSyntaxError(f"invalid number of arguments for instruction {rem_com_li[0]}")
            if rem_com_li[1] not in m.get_memory_keys():
                raise InterpreterSyntaxError(f"invalid label and/or memory address {rem_com_li[1]}")

        elif rem_com_li[0] in r_format:
            pass

        elif rem_com_li[0] in i_format:
            pass

        elif rem_com_li[0] in b_format:
            pass

        elif rem_com_li[0] in l_format:
            pass


    
    @staticmethod
    def get_all_instructions():
        return [ x for x in dir(Instructions) if not x.startswith("__") and x != "get_all_instructions" ]

    @staticmethod
    def extract_instruction_from_line(line):
        for i in Instructions.get_all_instructions():
            if i in line:
                return i
        
        return None

    @staticmethod
    def extract_label_from_line(line):
        if Instructions.isLabel(line):
            # remove the colon and get the label
            return line.split(":")[0].strip()

        return None

    @staticmethod
    def consume_directive_from_line(line):
        if Instructions.isDirective(line):
            split = line.split(" ")
            return {"directive": split[0], "value": " ".join(split[1::])}

        return None

    @staticmethod
    def isLabel(line):
        if ":" in line:
            return True
        return False

    @staticmethod
    def isDirective(line):
        if line.strip().startswith("."):
            return True
        return False

    @staticmethod
    def process_syscall(r, m, s):
        s.execute_syscall(r, m)

    @staticmethod
    def j():
        # raise an error to inform the user that control flow shoulnd't have reached here
        raise InterpreterControlFlowError("Invalid instruction j, control flow should not have reached here!")

    @staticmethod
    def jal():
        # raise an error to inform the user that control flow shoulnd't have reached here
        raise InterpreterControlFlowError("Invalid instruction jal, control flow should not have reached here!")

    @staticmethod
    def li(r, reg, val):
        if reg[0] != "$":
            raise InterpreterRegisterError("Invalid register name")

        r.set_register(reg[1:], int(val))

    @staticmethod
    def la(r, m, reg, val):
        if reg[0] != "$":
            raise InterpreterRegisterError("Invalid register name")

        r.set_register(reg[1:], m.get_address(val))

    @staticmethod
    def move(r, reg_save, reg_get):
        if reg_save[0] != "$" or reg_get[0] != "$":
            raise InterpreterRegisterError("Invalid register name")

        r.set_register(reg_save[1:], r.get_register(reg_get[1:]))

    @staticmethod
    def addi(r, reg_save, reg_get, val):
        if reg_save[0] != "$" and reg_get[0] != "$":
            raise InterpreterRegisterError("Invalid register name")
        if reg_save[1] == "t" and reg_get[1] == "t":
            r.set_temporary_register(reg_save[1:], r.get_temporary_register(reg_get[1:]) + int(val))
            
    @staticmethod
    def sw(r, m, reg, val):
        if reg[0] != "$":
            raise InterpreterRegisterError("Invalid register name")

        m.store_existing_word(val, r.get_register(reg[1:]))

    @staticmethod
    def lw(r, m, reg, val):
        if reg[0] != "$":
            raise InterpreterRegisterError("Invalid register name")

        r.set_register(reg[1:], m.load_existing_word(val))

