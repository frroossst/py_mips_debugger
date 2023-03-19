class InterpreterException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
    
class InterpreterSyntaxError(InterpreterException):
    pass

class InterpreterProcessError(InterpreterException):
    pass

class InterpreterRegisterError(InterpreterException):
    pass

class InterpreterControlFlowError(InterpreterException):
    pass

class InterpreterValueError(InterpreterException):
    pass

class InterpreterRuntimeError(InterpreterException):
    pass

class InterpreterTypeError(InterpreterException):
    pass

class InterpreterInstructionError(InterpreterException):
    pass

class InterpreterBreakpointError(InterpreterException):
    pass

class InterpreterLabelError(InterpreterException):
    pass

class InterpreterFileError(InterpreterException):
    pass

class InterpreterMemoryError(InterpreterException):
    pass

class InterpreterStackError(InterpreterException):
    pass

