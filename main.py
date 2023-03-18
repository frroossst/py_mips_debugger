from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from termcolor import cprint

from interpreter import Interpreter
from registers import Registers
from ide import IDE
import argparse
import sys


parser = argparse.ArgumentParser(description="A minimal MIPS assembly emulator written in Python")
parser.add_argument("file_name")
parser.add_argument("--no-gui", dest="no_gui_arg", action="store_true")
args = parser.parse_args()

R = None

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

    ide = IDE(file_name)
    ide.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    err_flag = False
    turn_on_gui = not args.no_gui_arg
    try:
        # show pre-alpha warning
        fmt = "WARNING: This is a pre-alpha version of the emulator. It is not guaranteed to work."
        cprint(fmt, "yellow", attrs=["bold", "blink"], file=sys.stderr)

        if len(sys.argv) < 2:
            raise ValueError("No file name provided")
        file_name = sys.argv[1]

        if turn_on_gui:
            setup_ide()
        else:
            fmt = f"Running {file_name} in CLI mode"
            cprint(fmt, "white", attrs=["reverse"], file=sys.stdout)

            R = Registers()
            I = Interpreter(file_name, R)
            I.process()
            I.run()

    except Exception as e:
        err = f"Emulator errored out with errror: {e}"
        err_flag = True
        cprint(err, "red", attrs=["bold"], file=sys.stderr)
    finally:
        print(R.__str__())

    if err_flag:
        fmt = "[ERROR]"
        cprint(fmt, "red", attrs=["bold"], file=sys.stderr)
    else:
        fmt = "[SUCCESS]"
        cprint(fmt, "green", attrs=["bold"], file=sys.stdout)
