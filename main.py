from interpreter import Interpreter
from registers import Registers
import sys


file = sys.argv[1]

if __name__ == '__main__':
    I = Interpreter(file)
    R = Registers()
    I.run()
    print(R)
