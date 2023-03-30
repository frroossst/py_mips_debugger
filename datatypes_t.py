from exceptions import InterpreterOverflow, InterpreterUnderflow, InterpreterTypeError

class uint8_t:

    value = None

    def check_bounds(self, value):
        if value > 255:
            raise InterpreterOverflow("Value too large for uint8_t")
        if value < 0:
            raise InterpreterUnderflow("Value too small for uint8_t")

    def __init__(self, value) -> None:
        self.check_bounds(value)

        self.value = value

    def __repr__(self) -> str:
        return f"uint8_t({self.value})"

    def __add__(self, other):
        if not isinstance(other, uint8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for +: 'uint8_t' and '{type(other).__name__}'")

        result = self.value + other.value

        self.check_bounds(result)

        return uint8_t(result)

    def __sub__(self, other):
        if not isinstance(other, uint8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for -: 'uint8_t' and '{type(other).__name__}'")

        result = self.value - other.value

        self.check_bounds(result)

        return uint8_t(result)

    def __mul__(self, other):
        if not isinstance(other, uint8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for *: 'uint8_t' and '{type(other).__name__}'")

        result = self.value * other.value

        self.check_bounds(result)

        return uint8_t(result)
    
    def __truediv__(self, other):
        if not isinstance(other, uint8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for /: 'uint8_t' and '{type(other).__name__}'")

        result = self.value / other.value

        self.check_bounds(result)

        return uint8_t(result)
    
    def __floordiv__(self, other):
        if not isinstance(other, uint8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for //: 'uint8_t' and '{type(other).__name__}'")

        result = self.value // other.value

        self.check_bounds(result)

        return uint8_t(result)
    
    def __mod__(self, other):
        if not isinstance(other, uint8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for %: 'uint8_t' and '{type(other).__name__}'")

        result = self.value % other.value

        self.check_bounds(result)

        return uint8_t(result)
    
class int8_t:
    pass

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
