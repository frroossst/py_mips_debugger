from PyQt5.QtCore import QObject, pyqtSignal

from exceptions import InterpreterExit, InterpreterSyscallError

class Syscall(QObject):

    console_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def execute_syscall(self, r, m):
        console_object = {
            "operation": None,
            "type": None,
            "data" : None
        }

        code_v0 = r.get_register("v0")

        # print int
        if code_v0 == 1:
            stdout_int = r.get_register("a0")
            console_object["operation"] = "stdout"
            console_object["type"] = "int"
            console_object["data"] = str(stdout_int)

        # print the string
        elif code_v0 == 4:
            stdout_str = m.get_string(r.get_register("a0"))
            console_object["operation"] = "stdout"
            console_object["type"] = "string"
            console_object["data"] = stdout_str

        # read int
        elif code_v0 == 5:
            console_object["operation"] = "stdin"
            console_object["type"] = "int"
            console_object["data"] = None

        # exit
        elif code_v0 == 10:
            raise InterpreterExit("Program exited", exit_code=0)

        # exit2 i.e. exit with a process code
        elif code_v0 == 17:
            raise InterpreterExit("Program exited", exit_code=r.get_register("a0"))

        else:
            raise InterpreterSyscallError("Invalid syscall code")

        self.console_signal.emit(console_object)