class Registers:

    register_value_changed = None

    # TODO: add register print formatters
    # print in hexadecimal, octal
    # print only some registers etc.

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

    # return address
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
        floating_point_registers = f"f0:  {self.f0} \nf1:  {self.f1} \nf2:  {self.f2} \nf3:  {self.f3} \nf4:  {self.f4} \nf5:  {self.f5} \nf6:  {self.f6} \nf7:  {self.f7} \nf8:  {self.f8} \nf9:  {self.f9} \nf10: {self.f10} \nf11: {self.f11} \nf12: {self.f12} \nf13: {self.f13} \nf14: {self.f14} \nf15: {self.f15} \nf16: {self.f16} \nf17: {self.f17} \nf18: {self.f18} \nf19: {self.f19} \nf20: {self.f20} \nf21: {self.f21} \nf22: {self.f22} \nf23: {self.f23} \nf24: {self.f24} \nf25: {self.f25} \nf26: {self.f26} \nf27: {self.f27} \nf28: {self.f28} \nf29: {self.f29} \nf30: {self.f30} \nf31: {self.f31}\n"
        fmt = f"{value_registers}\n{argument_registers}\n{temporary_registers}\n{saved_registers}\n{return_address}\n{floating_point_registers}"
        return fmt

    def set_temporary_register(self, register, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")

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
            raise ValueError(f"Invalid register name: {register}")
        
    def get_temporary_register(self, register):
        if register == "t0":
            return self.t0
        elif register == "t1":
            return self.t1
        elif register == "t2":
            return self.t2
        elif register == "t3":
            return self.t3
        elif register == "t4":
            return self.t4
        elif register == "t5":
            return self.t5
        elif register == "t6":
            return self.t6
        elif register == "t7":
            return self.t7
        elif register == "t8":
            return self.t8
        elif register == "t9":
            return self.t9
        else:
            raise ValueError("Invalid register name")
        
    def set_value_register(self, register, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")

        if register == "v0":
            self.v0 = value
        elif register == "v1":
            self.v1 = value
        else:
            raise ValueError("Invalid register name")
    
    def get_value_register(self, register):
        if register == "v0":
            return self.v0
        elif register == "v1":
            return self.v1
        else:
            raise ValueError("Invalid register name")
        
    def set_argument_register(self, register, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")

        if register == "a0":
            self.a0 = value
        elif register == "a1":
            self.a1 = value
        elif register == "a2":
            self.a2 = value
        elif register == "a3":
            self.a3 = value
        else:
            raise ValueError("Invalid register name")
        
    def get_argument_register(self, register):
        if register == "a0":
            return self.a0
        elif register == "a1":
            return self.a1
        elif register == "a2":
            return self.a2
        elif register == "a3":
            return self.a3
        else:
            raise ValueError("Invalid register name")
        
    def set_saved_register(self, register, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")

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
            raise ValueError("Invalid register name")
        
    def get_saved_register(self, register):
        if register == "s0":
            return self.s0
        elif register == "s1":
            return self.s1
        elif register == "s2":
            return self.s2
        elif register == "s3":
            return self.s3
        elif register == "s4":
            return self.s4
        elif register == "s5":
            return self.s5
        elif register == "s6":
            return self.s6
        elif register == "s7":
            return self.s7
        else:
            raise ValueError("Invalid register name")
        
    def set_return_address(self, value):
        self.ra = value

    def get_return_address(self):
        return self.ra
    
    def set_floating_point_register(self, register, value):
        if not isinstance(value, float):
            raise TypeError("Value must be a float")

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
            raise ValueError("Invalid register name")
        
    def get_floating_point_register(self, register):
        if register == "f0":
            return self.f0
        elif register == "f1":
            return self.f1
        elif register == "f2":
            return self.f2
        elif register == "f3":
            return self.f3
        elif register == "f4":
            return self.f4
        elif register == "f5":
            return self.f5
        elif register == "f6":
            return self.f6
        elif register == "f7":
            return self.f7
        elif register == "f8":
            return self.f8
        elif register == "f9":
            return self.f9
        elif register == "f10":
            return self.f10
        elif register == "f11":
            return self.f11
        elif register == "f12":
            return self.f12
        elif register == "f13":
            return self.f13
        elif register == "f14":
            return self.f14
        elif register == "f15":
            return self.f15
        elif register == "f16":
            return self.f16
        elif register == "f17":
            return self.f17
        elif register == "f18":
            return self.f18
        elif register == "f19":
            return self.f19
        elif register == "f20":
            return self.f20
        elif register == "f21":
            return self.f21
        elif register == "f22":
            return self.f22
        elif register == "f23":
            return self.f23
        elif register == "f24":
            return self.f24
        elif register == "f25":
            return self.f25
        elif register == "f26":
            return self.f26
        elif register == "f27":
            return self.f27
        elif register == "f28":
            return self.f28
        elif register == "f29":
            return self.f29
        elif register == "f30":
            return self.f30
        elif register == "f31":
            return self.f31
        else:
            raise ValueError("Invalid register name")
