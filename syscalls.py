from PyQt5.QtCore import QObject, pyqtSignal

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

        # print the string
        if code_v0 == 4:
            stdout_str = m.get_string(r.get_register("a0"))
            console_object["operation"] = "stdout"
            console_object["type"] = "string"
            console_object["data"] = stdout_str

        self.console_signal.emit(console_object)