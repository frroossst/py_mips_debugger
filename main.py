from multiplexer import Multiplexer
from interpreter import Interpreter
from registers import Registers
from instructions import *
import sys


file = sys.argv[1]

if __name__ == '__main__':
    R = Registers()
    I = Interpreter(file, R)
    I.run()
    print(R)
