from PyQt5.QtWidgets import QApplication
from termcolor import cprint
from interpreter import Interpreter
from registers import Registers
from instructions import *
from ide import *
import sys

file_name = sys.argv[1]

turn_on_gui = True

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
    # show pre-alpha warning
    fmt = "WARNING: This is a pre-alpha version of the emulator. It is not guaranteed to work."
    cprint(fmt, "yellow", attrs=["bold", "blink"], file=sys.stderr)

    if turn_on_gui:
        setup_ide()
    else:
        fmt = f"Running {file_name} in CLI mode"
        cprint(fmt, "white", attrs=["reverse"], file=sys.stdout)

    # setting up the runtime environment
    R = Registers()
    I = Interpreter(file_name, R)
    I.process()

    err_flag = False

    try:
        I.run()
    except Exception as e:
        err_flag = True
        err = f"Emulator errored out with errror: {e}"
        cprint(err, "red", attrs=["bold"], file=sys.stderr)
    finally:
        print(R)

    if err_flag:
        fmt = "[ERROR]"
        cprint(fmt, "red", attrs=["bold"], file=sys.stderr)
    else:
        fmt = "[SUCCESS]"
        cprint(fmt, "green", attrs=["bold"], file=sys.stdout)
