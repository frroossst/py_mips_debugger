from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from termcolor import cprint

from exceptions import InterpreterException
from configuration import Configuration
from interpreter import Interpreter
from registers import Registers
from syscalls import Syscall
from memory import Memory
from ide import IDE
import argparse
import sys


parser = argparse.ArgumentParser(description="A minimal MIPS assembly emulator written in Python")
parser.add_argument("--no-gui", dest="no_gui_arg", action="store_true")
args = parser.parse_args()



def exception_hook(exctype, value, traceback):

    if (issubclass(exctype, InterpreterException)):
        if value.message == "Program exited":
            print(f"Program exited with exit code: {value.exit_code}")
            return None # this was expected, so continue with the GUI, but stop the Interpreter

        # print last known state of registers
        print("*" * 80)
        registers_ref = ide.R # from the ide global
        memory_ref   = ide.M 
        print("Last known state of registers:")
        print(registers_ref.__str__())
        print("Last known state of memory:")
        print(memory_ref.__str__())

        fmt = "[ERROR]"
        cprint(fmt, "red", attrs=["bold"], file=sys.stderr, end=" ")
        err = f"Emulator errored out with error: {str(exctype.__name__)}: {str(value)}"
        cprint(err, "red", attrs=["bold"], file=sys.stderr)
        print(f"label: {value.label_that_crashed} (instruction: {value.instruction_that_crashed})")

        print("\nPlease report this to the developer, if you think this was unexpected.")
        link = "https://github.com/frroossst/py_mips_debugger/issues/new"
        cprint(f"{link}\n", "blue", attrs=["underline"])

        sys.exit(1) 

    elif issubclass(exctype, KeyboardInterrupt):
        sys.exit(1)

    else:
        sys.__excepthook__(exctype, value, traceback)

# setting up the GUI
def setup_ide():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    global ide
    ide = IDE(file_name)
    ide.show()
    sys.excepthook = exception_hook
    sys.exit(app.exec_())

if __name__ == '__main__':
    turn_on_gui = not args.no_gui_arg

    # show pre-alpha warning
    fmt = "WARNING: This is a pre-alpha version of the emulator. It is not guaranteed to work as expected."
    cprint(fmt, "yellow", attrs=["bold", "blink"], file=sys.stderr)

    file_name = Configuration().get_config("file_to_run")

    if turn_on_gui:
        setup_ide()
    else:
        fmt = f"Running {file_name} in CLI mode"
        cprint(fmt, "white", attrs=["reverse"], file=sys.stdout)

        R = Registers()
        M = Memory()
        S = Syscall()
        I = Interpreter(file_name, R, M, S)
        I.process()
        I.run()