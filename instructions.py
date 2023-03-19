from exceptions import InterpreterControlFlowError, InterpreterRegisterError

class Instructions:

    @staticmethod
    def get_all_instructions():
        return [ x for x in dir(Instructions) if not x.startswith("__") and x != "get_all_instructions" ]

    @staticmethod
    def isLabel(line):
        if ":" in line:
            return True
        return False

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
        if reg[1] == "t":
            r.set_temporary_register(reg[1:], int(val))

    @staticmethod
    def addi(r, reg_save, reg_get, val):
        if reg_save[0] != "$" and reg_get[0] != "$":
            raise InterpreterRegisterError("Invalid register name")
        if reg_save[1] == "t" and reg_get[1] == "t":
            r.set_temporary_register(reg_save[1:], r.get_temporary_register(reg_get[1:]) + int(val))

