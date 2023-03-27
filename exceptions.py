class InterpreterException(Exception):

    def __init__(self, message, label_that_crashed=None, instruction_that_crashed=None, exit_code=None):
        if self.__class__ is InterpreterException:
            raise TypeError("InterpreterException is an abstract class and cannot be instantiated")
        self.message = message
        self.label_that_crashed = label_that_crashed
        self.instruction_that_crashed = instruction_that_crashed
        self.exit_code = exit_code
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

class InterpreterConversionError(InterpreterException):
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

class InterpreterRecursionError(InterpreterException):
    pass

class InterpreterMemoryError(InterpreterException):
    pass

class InterpreterStackError(InterpreterException):
    pass

class InterpreterSyscallError(InterpreterException):
    pass

class InterpreterExit(InterpreterException):
    pass

class InterpreterTooLargeToFit(InterpreterException):
    pass

class InterpreterTooSmallToFit(InterpreterException):
    pass

class InterpreterOverflow(InterpreterException):
    pass

class InterpreterUnderflow(InterpreterException):
    pass



