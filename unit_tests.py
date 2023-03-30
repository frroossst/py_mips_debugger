from datatypes_t import *
from exceptions import *

# testing datatypes_t
count = 0
for i in range(0, 256):
    result = uint8_t(i).unwrap()
    expected = i
    assert result == expected, f"Expected {expected}, got {result}"

for i in range(-256, 0):
    expected = None
    try:
        result = int8_t(i).unwrap()
        assert result == expected, f"Expected {expected}, got {result}"
    except InterpreterOverflow:
        pass

result = uint8_t(55) + uint8_t(1)
expected = uint8_t(56)
assert result.unwrap() == expected.unwrap(), f"Expected {expected}, got {result}"

result = uint8_t(55) - uint8_t(1)
expected = uint8_t(54)
assert result.unwrap() == expected.unwrap(), f"Expected {expected}, got {result}"

exit(0)
