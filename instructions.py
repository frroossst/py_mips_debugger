from exceptions import InterpreterControlFlowError, InterpreterRegisterError

class Instructions:
    
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
    def addi(r, reg_save, reg_get, val):
        if reg_save[0] != "$" and reg_get[0] != "$":
            raise InterpreterRegisterError("Invalid register name")
        if reg_save[1] == "t" and reg_get[1] == "t":
            r.set_temporary_register(reg_save[1:], r.get_temporary_register(reg_get[1:]) + int(val))

