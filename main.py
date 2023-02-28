from breakpoints import GLOBAL_BREAKPOINTS
from PyQt5.QtWidgets import QApplication
from multiplexer import Multiplexer
from interpreter import Interpreter
from registers import Registers
from instructions import *
from ide import *
import sys

file_name = sys.argv[1]
GLOBAL_BREAKPOINTS = {}

# setting up the GUI
def setup_ide():
    app = QApplication(sys.argv)
    ide = IDE(file_name)
    ide.show()
    sys.exit(app.exec_())

def setup_runtime():
    R = Registers()
    I = Interpreter(file_name, R)
    I.process()
    I.run()

if __name__ == '__main__':
    setup_ide()

    # setting up the runtime environment
    # R = Registers()
    # I = Interpreter(file_name, R)
    # I.process()

    try:
        I.run()
    except Exception as e:
        print(f"Emulator errored out with errror: {e}")
    finally:
        print(R)
