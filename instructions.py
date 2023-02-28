from copy import copy

class Instuctions:

    @staticmethod
    def get_all_instructions():
        return [ x for x in dir(Instuctions) if not x.startswith("__") and x != "get_all_instructions" ]

    @staticmethod
    def isLabel(line):
        if ":" in line:
            return True
        return False

    @staticmethod
    def j():
        # raise an error to inform the user that control flow shoulnd't have reached here
        raise RuntimeError("Invalid instruction j, control flow should not have reached here!")

    @staticmethod
    def li(r, reg, val):
        if reg[0] != "$":
            raise ValueError("Invalid register name")
        if reg[1] == "t":
            r.set_temporary_register(reg[1:], int(val))

    @staticmethod
    def addi(r, reg, val):
        if reg[0] != "$":
            raise ValueError("Invalid register name")
        if reg[1] == "t":
            r.set_temporary_register(reg[1:], r.get_temporary_register(reg[1:]) + int(val))

