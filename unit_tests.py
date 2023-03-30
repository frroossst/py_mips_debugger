from datatypes_t import *
from exceptions import *

# testing datatypes_t
count = 0
for i in range(0, 256):
    result = uint8_t(i).value
    expected = i
    assert result == expected, f"Expected {expected}, got {result}"

result = uint8_t(55) + uint8_t(1)
expected = uint8_t(56).value
assert result.value == expected, f"Expected {expected}, got {result}"

result = uint8_t(55) - uint8_t(1)
expected = uint8_t(54).value
assert result.value == expected, f"Expected {expected}, got {result}"

exit(0)
