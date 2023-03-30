from exceptions import InterpreterOverflow, InterpreterUnderflow, InterpreterTypeError
import struct

class uint8_t:

    value = None

    def __init__(self, value) -> None:
        if value > 255:
            raise InterpreterOverflow("Value too large for uint8_t")
        if value < 0:
            raise InterpreterUnderflow("Value too small for uint8_t")

        self.value = struct.pack("H", value)

    def __repr__(self) -> str:
        return f"uint8_t({int.from_bytes(self.value, 'little')})"

    def unwrap(self):
        return int.from_bytes(self.value, 'little')

    def __add__(self, other):
        if not isinstance(other, uint8_t):
            raise InterpreterTypeError("unsupported operand type(s) for +: 'uint8_t' and '{}'".format(type(other).__name__))

        curr = int.from_bytes(self.value, 'little')
        other = int.from_bytes(other.value, 'little')

        result = curr + other

        if result > 255:
            raise InterpreterOverflow("uint8_t addition resulted in overflow")

        return uint8_t(result)

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

        self.value = struct.pack("h", value)

    def __repr__(self) -> str:
        return f"int8_t({int.from_bytes(self.value, 'little')})"

    def unwrap(self):
        return int.from_bytes(self.value, 'little')

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

    def __init__(self, value) -> None:
        if value > 4294967295:
            raise InterpreterOverflow("Value too large for uint32_t")
        if value < 0:
            raise InterpreterUnderflow("Value too small for uint32_t")

        self.value = struct.pack("I", value)

    def __repr__(self) -> str:
        return f"uint32_t({int.from_bytes(self.value, 'little')})"

    def unwrap(self):
        return int.from_bytes(self.value, 'little')
    
    def __add__(self, other):
        if not isinstance(other, uint32_t):
            raise InterpreterTypeError("unsupported operand type(s) for +: 'uint32_t' and '{}'".format(type(other).__name__))

        curr = int.from_bytes(self.value, 'little')
        other = int.from_bytes(other.value, 'little')

        result = curr+ other

        if result > 4294967295:
            raise InterpreterOverflow("uint32_t addition resulted in overflow")

        return uint32_t(result)
    
    def __sub__(self, other):
        sum_num = self.value - other.value
        if sum_num.bit_length() > 32:
            raise InterpreterOverflow("Overflow while subtracting uint32_t")

        return uint32_t(sum_num)
    
class int32_t:
    pass

class f32_t:
    pass

class f64_t:
    pass
