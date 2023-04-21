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
    
    def __mod__(self, other):
        if not isinstance(other, uint8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for %: 'uint8_t' and '{type(other).__name__}'")

        result = self.value % other.value

        self.check_bounds(result)

        return uint8_t(result)
    
class int8_t:
    
    value = None

    def check_bounds(self, value):
        if value > 127:
            raise InterpreterOverflow("Value too large for int8_t")
        if value < -128:
            raise InterpreterUnderflow("Value too small for int8_t")
        
    def __init__(self, value) -> None:
        self.check_bounds(value)

        self.value = value

    def __repr__(self) -> str:
        return f"int8_t({self.value})"
    
    def __add__(self, other):
        if not isinstance(other, int8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for +: 'int8_t' and '{type(other).__name__}'")

        result = self.value + other.value

        self.check_bounds(result)

        return int8_t(result)
    
    def __sub__(self, other):
        if not isinstance(other, int8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for -: 'int8_t' and '{type(other).__name__}'")

        result = self.value - other.value

        self.check_bounds(result)

        return int8_t(result)
    
    def __mul__(self, other):
        if not isinstance(other, int8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for *: 'int8_t' and '{type(other).__name__}'")

        result = self.value * other.value

        self.check_bounds(result)

        return int8_t(result)
    
    def __truediv__(self, other):
        if not isinstance(other, int8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for /: 'int8_t' and '{type(other).__name__}'")

        result = self.value / other.value

        self.check_bounds(result)

        return int8_t(result)
    
    def __mod__(self, other):
        if not isinstance(other, int8_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for %: 'int8_t' and '{type(other).__name__}'")

        result = self.value % other.value

        self.check_bounds(result)

        return int8_t(result)
    
class uint16_t:

    value = None

    def check_bounds(self, value):
        if value > 65535:
            raise InterpreterOverflow("Value too large for uint16_t")
        if value < 0:
            raise InterpreterUnderflow("Value too small for uint16_t")
        
    def __init__(self, value) -> None:
        self.check_bounds(value)

        self.value = value

    def __repr__(self) -> str:
        return f"uint16_t({self.value})"
    
    def __add__(self, other):
        if not isinstance(other, uint16_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for +: 'uint16_t' and '{type(other).__name__}'")

        result = self.value + other.value

        self.check_bounds(result)

        return uint16_t(result)
    
    def __sub__(self, other):
        if not isinstance(other, uint16_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for -: 'uint16_t' and '{type(other).__name__}'")

        result = self.value - other.value

        self.check_bounds(result)

        return uint16_t(result)
    
    def __mul__(self, other):
        if not isinstance(other, uint16_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for *: 'uint16_t' and '{type(other).__name__}'")

        result = self.value * other.value

        self.check_bounds(result)

        return uint16_t(result)
    
    def __truediv__(self, other):
        if not isinstance(other, uint16_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for /: 'uint16_t' and '{type(other).__name__}'")

        result = self.value / other.value

        self.check_bounds(result)

        return uint16_t(result)
    
    def __mod__(self, other):
        if not isinstance(other, uint16_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for %: 'uint16_t' and '{type(other).__name__}'")

        result = self.value % other.value

        self.check_bounds(result)

        return uint16_t(result)
    
class int16_t:

    value = None

    def check_bounds(self, value):
        if value > 32767:
            raise InterpreterOverflow("Value too large for int16_t")
        if value < -32768:
            raise InterpreterUnderflow("Value too small for int16_t")
        
    def __init__(self, value) -> None:
        self.check_bounds(value)

        self.value = value

    def __repr__(self) -> str:
        return f"int16_t({self.value})"
    
    def __add__(self, other):
        if not isinstance(other, int16_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for +: 'int16_t' and '{type(other).__name__}'")

        result = self.value + other.value

        self.check_bounds(result)

        return int16_t(result)
    
    def __sub__(self, other):
        if not isinstance(other, int16_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for -: 'int16_t' and '{type(other).__name__}'")

        result = self.value - other.value

        self.check_bounds(result)

        return int16_t(result)
    
    def __mul__(self, other):
        if not isinstance(other, int16_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for *: 'int16_t' and '{type(other).__name__}'")

        result = self.value * other.value

        self.check_bounds(result)

        return int16_t(result)
    
    def __truediv__(self, other):
        if not isinstance(other, int16_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for /: 'int16_t' and '{type(other).__name__}'")

        result = self.value / other.value

        self.check_bounds(result)

        return int16_t(result)
    
    def __mod__(self, other):
        if not isinstance(other, int16_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for %: 'int16_t' and '{type(other).__name__}'")

        result = self.value % other.value

        self.check_bounds(result)

        return int16_t(result)

class uint32_t:
    
    value = None

    def check_bounds(self, value):
        if value > 4294967295:
            raise InterpreterOverflow("Value too large for uint32_t")
        if value < 0:
            raise InterpreterUnderflow("Value too small for uint32_t")
        
    def __init__(self, value) -> None:
        self.check_bounds(value)

        self.value = value

    def __repr__(self) -> str:
        return f"uint32_t({self.value})"
    
    def __add__(self, other):
        if not isinstance(other, uint32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for +: 'uint32_t' and '{type(other).__name__}'")

        result = self.value + other.value

        self.check_bounds(result)

        return uint32_t(result)
    
    def __sub__(self, other):
        if not isinstance(other, uint32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for -: 'uint32_t' and '{type(other).__name__}'")

        result = self.value - other.value

        self.check_bounds(result)

        return uint32_t(result)
    
    def __mul__(self, other):
        if not isinstance(other, uint32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for *: 'uint32_t' and '{type(other).__name__}'")

        result = self.value * other.value

        self.check_bounds(result)

        return uint32_t(result)
    
    def __truediv__(self, other):
        if not isinstance(other, uint32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for /: 'uint32_t' and '{type(other).__name__}'")

        result = self.value / other.value

        self.check_bounds(result)

        return uint32_t(result)
    
    def __mod__(self, other):
        if not isinstance(other, uint32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for %: 'uint32_t' and '{type(other).__name__}'")

        result = self.value % other.value

        self.check_bounds(result)

        return uint32_t(result)

class int32_t:

    value = None

    def check_bounds(self, value):
        if value > 2147483647:
            raise InterpreterOverflow("Value too large for int32_t")
        if value < -2147483648:
            raise InterpreterUnderflow("Value too small for int32_t")
        
    def __init__(self, value) -> None:
        self.check_bounds(value)

        self.value = value

    def __repr__(self) -> str:
        return f"int32_t({self.value})"
    
    def __add__(self, other):
        if not isinstance(other, int32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for +: 'int32_t' and '{type(other).__name__}'")

        result = self.value + other.value

        self.check_bounds(result)

        return int32_t(result)
    
    def __sub__(self, other):
        if not isinstance(other, int32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for -: 'int32_t' and '{type(other).__name__}'")

        result = self.value - other.value

        self.check_bounds(result)

        return int32_t(result)
    
    def __mul__(self, other):
        if not isinstance(other, int32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for *: 'int32_t' and '{type(other).__name__}'")

        result = self.value * other.value

        self.check_bounds(result)

        return int32_t(result)
    
    def __truediv__(self, other):
        if not isinstance(other, int32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for /: 'int32_t' and '{type(other).__name__}'")

        result = self.value / other.value

        self.check_bounds(result)

        return int32_t(result)
    
    def __mod__(self, other):
        if not isinstance(other, int32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for %: 'int32_t' and '{type(other).__name__}'")

        result = self.value % other.value

        self.check_bounds(result)

        return int32_t(result)

class float32_t:

    value = None

    def check_bounds(self, value):
        if value > 3.4028234663852886e+38:
            raise InterpreterOverflow("Value too large for f32_t")
        if value < -3.4028234663852886e+38:
            raise InterpreterUnderflow("Value too small for f32_t")
        
    def __init__(self, value) -> None:
        self.check_bounds(value)

        self.value = value

    def __repr__(self) -> str:
        return f"f32_t({self.value})"
    
    def __add__(self, other):
        if not isinstance(other, float32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for +: 'f32_t' and '{type(other).__name__}'")

        result = self.value + other.value

        self.check_bounds(result)

        return float32_t(result)
    
    def __sub__(self, other):
        if not isinstance(other, float32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for -: 'f32_t' and '{type(other).__name__}'")

        result = self.value - other.value

        self.check_bounds(result)

        return float32_t(result)
    
    def __mul__(self, other):
        if not isinstance(other, float32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for *: 'f32_t' and '{type(other).__name__}'")

        result = self.value * other.value

        self.check_bounds(result)

        return float32_t(result)
    
    def __truediv__(self, other):
        if not isinstance(other, float32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for /: 'f32_t' and '{type(other).__name__}'")

        result = self.value / other.value

        self.check_bounds(result)

        return float32_t(result)
    
    def __mod__(self, other):
        if not isinstance(other, float32_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for %: 'f32_t' and '{type(other).__name__}'")

        result = self.value % other.value

        self.check_bounds(result)

        return float32_t(result)

class float64_t:

    value = None

    def check_bounds(self, value):
        if value > 1.7976931348623157e+308:
            raise InterpreterOverflow("Value too large for f64_t")
        if value < -1.7976931348623157e+308:
            raise InterpreterUnderflow("Value too small for f64_t")
        
    def __init__(self, value) -> None:
        self.check_bounds(value)

        self.value = value

    def __repr__(self) -> str:
        return f"f64_t({self.value})"
    
    def __add__(self, other):
        if not isinstance(other, float64_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for +: 'f64_t' and '{type(other).__name__}'")

        result = self.value + other.value

        self.check_bounds(result)

        return float64_t(result)
    
    def __sub__(self, other):
        if not isinstance(other, float64_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for -: 'f64_t' and '{type(other).__name__}'")

        result = self.value - other.value

        self.check_bounds(result)

        return float64_t(result)
    
    def __mul__(self, other):
        if not isinstance(other, float64_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for *: 'f64_t' and '{type(other).__name__}'")

        result = self.value * other.value

        self.check_bounds(result)

        return float64_t(result)
    
    def __truediv__(self, other):
        if not isinstance(other, float64_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for /: 'f64_t' and '{type(other).__name__}'")

        result = self.value / other.value

        self.check_bounds(result)

        return float64_t(result)
    
    def __mod__(self, other):
        if not isinstance(other, float64_t):
            raise InterpreterTypeError(f"unsupported operand type(s) for %: 'f64_t' and '{type(other).__name__}'")

        result = self.value % other.value

        self.check_bounds(result)

        return float64_t(result)