class Instuctions:

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