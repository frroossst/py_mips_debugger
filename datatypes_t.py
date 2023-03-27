from exceptions import InterpreterOverflow, InterpreterUnderflow

class twos_complement:

    value = 0

    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return str(f"{self.__class__.__name__}({self.value})")

    def get_value(self):
        return self.value

class uint8_t(twos_complement):

    def __init__(self, value) -> None:
        if value > 255:
            raise InterpreterOverflow("Value too large for uint8_t")
        if value < 0:
            raise InterpreterUnderflow("Value too small for uint8_t")

        super().__init__(value)

    def __add__(self, other):
        sum_num = self.value + other.value
        if sum_num.bit_length() > 8:
            raise InterpreterOverflow("Overflow while adding uint8_t")

        return uint8_t(sum_num)

    def __sub__(self, other):
        sum_num = self.value - other.value
        if sum_num.bit_length() > 8:
            raise InterpreterOverflow("Overflow while subtracting uint8_t")

        return uint8_t(sum_num)

class int8_t:

    def __init__(self, value) -> None:
        if value > 127:
            raise InterpreterOverflow("Value too large for int8_t")
        if value < -128:
            raise InterpreterUnderflow("Value too small for int8_t")

        super().__init__(value)

    def __add__(self, other):
        sum_num = self.value + other.value
        if sum_num.bit_length() > 8:
            raise InterpreterOverflow("Overflow while adding int8_t")

        return int8_t(sum_num)

    def __sub__(self, other):
        sum_num = self.value - other.value
        if sum_num.bit_length() > 8:
            raise InterpreterOverflow("Overflow while subtracting int8_t")

        return int8_t(sum_num)

class uint16_t:
    pass

class int16_t:
    pass

class uint32_t:
    pass

class int32_t:
    pass

class f32_t:
    pass

class f64_t:
    pass
