from exceptions import InterpreterRegisterError, InterpreterTypeError

class Registers:

    # TODO: add register print formatters
    # print in hexadecimal, octal
    # print only some registers etc.

    register_hotmap = []

    # $zero
    zero = 0

    # value registers
    v0 = 0
    v1 = 0

    # argument registers
    a0 = 0
    a1 = 0
    a2 = 0
    a3 = 0

    # temporary registers
    t0 = 0
    t1 = 0
    t2 = 0
    t3 = 0
    t4 = 0
    t5 = 0
    t6 = 0
    t7 = 0
    t8 = 0
    t9 = 0

    # saved registers
    s0 = 0
    s1 = 0
    s2 = 0
    s3 = 0
    s4 = 0
    s5 = 0
    s6 = 0
    s7 = 0

    # register return address
    ra = 0

    # floating point registers
    f0 = 0.0
    f1 = 0.0
    f2 = 0.0
    f3 = 0.0
    f4 = 0.0
    f5 = 0.0
    f6 = 0.0
    f7 = 0.0
    f8 = 0.0
    f9 = 0.0
    f10 = 0.0
    f11 = 0.0
    f12 = 0.0
    f13 = 0.0
    f14 = 0.0
    f15 = 0.0
    f16 = 0.0
    f17 = 0.0
    f18 = 0.0
    f19 = 0.0
    f20 = 0.0
    f21 = 0.0
    f22 = 0.0
    f23 = 0.0
    f24 = 0.0
    f25 = 0.0
    f26 = 0.0
    f27 = 0.0
    f28 = 0.0
    f29 = 0.0
    f30 = 0.0
    f31 = 0.0

    hi = 0
    lo = 0


    def __init__(self):
        pass

    # returns the values of all the registers as strings
    def __str__(self):
        value_registers = f"v0: {self.v0} \nv1: {self.v1}\n"
        argument_registers = f"a0: {self.a0} \na1: {self.a1} \na2: {self.a2} \na3: {self.a3}\n"
        temporary_registers = f"t0: {self.t0} \nt1: {self.t1} \nt2: {self.t2} \nt3: {self.t3} \nt4: {self.t4} \nt5: {self.t5} \nt6: {self.t6} \nt7: {self.t7} \nt8: {self.t8} \nt9: {self.t9}\n"
        saved_registers = f"s0: {self.s0} \ns1: {self.s1} \ns2: {self.s2} \ns3: {self.s3} \ns4: {self.s4} \ns5: {self.s5} \ns6: {self.s6} \ns7: {self.s7}\n"
        return_address = f"ra: {self.ra}\n"
        hi_lo = f"hi: {self.hi} \nlo: {self.lo}\n"
        floating_point_registers = f"f0:  {self.f0} \nf1:  {self.f1} \nf2:  {self.f2} \nf3:  {self.f3} \nf4:  {self.f4} \nf5:  {self.f5} \nf6:  {self.f6} \nf7:  {self.f7} \nf8:  {self.f8} \nf9:  {self.f9} \nf10: {self.f10} \nf11: {self.f11} \nf12: {self.f12} \nf13: {self.f13} \nf14: {self.f14} \nf15: {self.f15} \nf16: {self.f16} \nf17: {self.f17} \nf18: {self.f18} \nf19: {self.f19} \nf20: {self.f20} \nf21: {self.f21} \nf22: {self.f22} \nf23: {self.f23} \nf24: {self.f24} \nf25: {self.f25} \nf26: {self.f26} \nf27: {self.f27} \nf28: {self.f28} \nf29: {self.f29} \nf30: {self.f30} \nf31: {self.f31}\n"
        return f"{value_registers}\n{argument_registers}\n{temporary_registers}\n{saved_registers}\n{return_address}\n{hi_lo}\n{floating_point_registers}"

    def clear_registers(self):
        all_registers = [
            "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9",
            "s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
            "v0", "v1",
            "a0", "a1", "a2", "a3",
            "ra",
            "hi", "lo",
            "f0", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f20", "f21", "f22", "f23", "f24", "f25", "f26", "f27", "f28", "f29", "f30", "f31"
            ]
        for register in all_registers:
            self.set_register(register, 0)

    def add_to_register_hotmap(self, register):
        if register in self.register_hotmap:
            self.register_hotmap.remove(register)
        
        if len(self.register_hotmap) >= 3:
            self.register_hotmap.pop(0)
            self.register_hotmap.append(register)
        else:
            self.register_hotmap.append(register)

    def set_register(self, register, value):
        if register[0] == "t":
            self.set_temporary_register(register, value)
        elif register[0] == "s":
            self.set_saved_register(register, value)
        elif register[0] == "v":
            self.set_value_register(register, value)
        elif register[0] == "a":
            self.set_argument_register(register, value)
        elif register[0] == "r":
            self.set_return_address(value)
        elif register == "hi":
            self.set_hi_register(value)
        elif register == "lo":
            self.set_lo_register(value)
        elif register[0] == "f":
            self.set_floating_point_register(register, float(value))
        else:
            raise InterpreterRegisterError(f"Invalid register name: {register}")

    def get_register(self, register):
        if register[0] == "t":
            return self.get_temporary_register(register)
        if register[0] == "s":
            return self.get_saved_register(register)
        if register[0] == "v":
            return self.get_value_register(register)
        if register[0] == "a":
            return self.get_argument_register(register)
        if register[0] == "r":
            return self.get_return_address()
        if register == "hi":
            return self.get_hi_register()
        if register == "lo":
            return self.get_lo_register()
        if register[0] == "f":
            return self.get_floating_point_register(register)

        raise InterpreterRegisterError(f"Invalid register name: {register}")

    def set_temporary_register(self, register, value):
        if not isinstance(value, int):
            raise InterpreterTypeError("Value must be an integer")

        if register == "t0":
            self.t0 = value
        elif register == "t1":
            self.t1 = value
        elif register == "t2":
            self.t2 = value
        elif register == "t3":
            self.t3 = value
        elif register == "t4":
            self.t4 = value
        elif register == "t5":
            self.t5 = value
        elif register == "t6":
            self.t6 = value
        elif register == "t7":
            self.t7 = value
        elif register == "t8":
            self.t8 = value
        elif register == "t9":
            self.t9 = value
        else:
            raise InterpreterRegisterError(f"Invalid register name: {register}")

        self.add_to_register_hotmap(register)

    def get_temporary_register(self, register):
        if register == "t0":
            return self.t0
        if register == "t1":
            return self.t1
        if register == "t2":
            return self.t2
        if register == "t3":
            return self.t3
        if register == "t4":
           return self.t4
        if register == "t5":
            return self.t5
        if register == "t6":
            return self.t6
        if register == "t7":
            return self.t7
        if register == "t8":
            return self.t8
        if register == "t9":
            return self.t9

        raise InterpreterRegisterError("Invalid register name")
        
    def set_value_register(self, register, value):
        if not isinstance(value, int):
            raise InterpreterTypeError("Value must be an integer")

        if register == "v0":
            self.v0 = value
        elif register == "v1":
            self.v1 = value
        else:
            raise InterpreterRegisterError("Invalid register name")

        self.add_to_register_hotmap(register)
    
    def get_value_register(self, register):
        if register == "v0":
            return self.v0
        if register == "v1":
            return self.v1

        raise InterpreterRegisterError("Invalid register name")
        
    def set_argument_register(self, register, value):
        if not isinstance(value, int):
            raise InterpreterTypeError("Value must be an integer")

        if register == "a0":
            self.a0 = value
        elif register == "a1":
            self.a1 = value
        elif register == "a2":
            self.a2 = value
        elif register == "a3":
            self.a3 = value
        else:
            raise InterpreterRegisterError("Invalid register name")

        self.add_to_register_hotmap(register)
        
    def get_argument_register(self, register):
        if register == "a0":
            return self.a0
        if register == "a1":
            return self.a1
        if register == "a2":
            return self.a2
        if register == "a3":
            return self.a3

        raise InterpreterRegisterError("Invalid register name")
        
    def set_saved_register(self, register, value):
        if not isinstance(value, int):
            raise InterpreterTypeError("Value must be an integer")

        if register == "s0":
            self.s0 = value
        elif register == "s1":
            self.s1 = value
        elif register == "s2":
            self.s2 = value
        elif register == "s3":
            self.s3 = value
        elif register == "s4":
            self.s4 = value
        elif register == "s5":
            self.s5 = value
        elif register == "s6":
            self.s6 = value
        elif register == "s7":
            self.s7 = value
        else:
            raise InterpreterRegisterError("Invalid register name")

        self.add_to_register_hotmap(register)
        
    def get_saved_register(self, register):
        if register == "s0":
            return self.s0
        if register == "s1":
            return self.s1
        if register == "s2":
            return self.s2
        if register == "s3":
            return self.s3
        if register == "s4":
            return self.s4
        if register == "s5":
            return self.s5
        if register == "s6":
            return self.s6
        if register == "s7":
            return self.s7

        raise InterpreterRegisterError("Invalid register name")
        
    def set_return_address(self, value):
        self.ra = value

        self.add_to_register_hotmap("ra")

    def get_return_address(self):
        return self.ra

    def set_hi_register(self, value):
        self.hi = value

        self.add_to_register_hotmap("hi")

    def get_hi_register(self):
        return self.hi
    
    def set_lo_register(self, value):
        self.lo = value

        self.add_to_register_hotmap("lo")

    def get_lo_register(self):
        return self.lo
    
    def set_floating_point_register(self, register, value):
        if not isinstance(value, float):
            raise InterpreterTypeError("Value must be a float")

        if register == "f0":
            self.f0 = value
        elif register == "f1":
            self.f1 = value
        elif register == "f2":
            self.f2 = value
        elif register == "f3":
            self.f3 = value
        elif register == "f4":
            self.f4 = value
        elif register == "f5":
            self.f5 = value
        elif register == "f6":
            self.f6 = value
        elif register == "f7":
            self.f7 = value
        elif register == "f8":
            self.f8 = value
        elif register == "f9":
            self.f9 = value
        elif register == "f10":
            self.f10 = value
        elif register == "f11":
            self.f11 = value
        elif register == "f12":
            self.f12 = value
        elif register == "f13":
            self.f13 = value
        elif register == "f14":
            self.f14 = value
        elif register == "f15":
            self.f15 = value
        elif register == "f16":
            self.f16 = value
        elif register == "f17":
            self.f17 = value
        elif register == "f18":
            self.f18 = value
        elif register == "f19":
            self.f19 = value
        elif register == "f20":
            self.f20 = value
        elif register == "f21":
            self.f21 = value
        elif register == "f22":
            self.f22 = value
        elif register == "f23":
            self.f23 = value
        elif register == "f24":
            self.f24 = value
        elif register == "f25":
            self.f25 = value
        elif register == "f26":
            self.f26 = value
        elif register == "f27":
            self.f27 = value
        elif register == "f28":
            self.f28 = value
        elif register == "f29":
            self.f29 = value
        elif register == "f30":
            self.f30 = value
        elif register == "f31":
            self.f31 = value
        else:
            raise InterpreterRegisterError("Invalid register name")

        self.add_to_register_hotmap(register)
        
    def get_floating_point_register(self, register):
        if register == "f0":
            return self.f0
        if register == "f1":
            return self.f1
        if register == "f2":
            return self.f2
        if register == "f3":
            return self.f3
        if register == "f4":
            return self.f4
        if register == "f5":
            return self.f5
        if register == "f6":
            return self.f6
        if register == "f7":
            return self.f7
        if register == "f8":
            return self.f8
        if register == "f9":
            return self.f9
        if register == "f10":
            return self.f10
        if register == "f11":
            return self.f11
        if register == "f12":
            return self.f12
        if register == "f13":
            return self.f13
        if register == "f14":
            return self.f14
        if register == "f15":
            return self.f15
        if register == "f16":
            return self.f16
        if register == "f17":
            return self.f17
        if register == "f18":
            return self.f18
        if register == "f19":
            return self.f19
        if register == "f20":
            return self.f20
        if register == "f21":
            return self.f21
        if register == "f22":
            return self.f22
        if register == "f23":
            return self.f23
        if register == "f24":
            return self.f24
        if register == "f25":
            return self.f25
        if register == "f26":
            return self.f26
        if register == "f27":
            return self.f27
        if register == "f28":
            return self.f28
        if register == "f29":
            return self.f29
        if register == "f30":
            return self.f30
        if register == "f31":
            return self.f31

        raise InterpreterRegisterError("Invalid register name")
