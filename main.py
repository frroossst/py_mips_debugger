from interpreter import Interpreter
import sys


file = sys.argv[1]

if __name__ == '__main__':
    interpreter = Interpreter.run(file)
