# exceptions.py

There is a general base/ parent class for all custom exceptions called InterpreterException which inherits from the 
in-built Exception class. This class is an abstract class cannot be instantiated on its own, you need to instantiate
one of it's many subclasses.

The InterpreterException class takes in a message that will be displayed to the user upon encountering the exception, 
it can also take in three optional keyword arguments: `label_that_crashed`, `instruction_that_crashed` and `exit_code`.

## Interpreter Exceptions

| Name | Description | Example |
|------|-------------|---------|
| InterpreterSyntaxError | when a syntax error is encountered in the assembly code | an empty label or out of place label |
| InterpreterProcessError | when functions are called out of the expected order | the Interpreter is run before the labels and memory is mapped |
| InterpreterRegisterError | when an invalid register is used | some value is set to register $t55 |
| InterpreterControlFlowError | when an unexpected control flow event occurs | the code has reached someplace it shouldn't, processing a jump instruction from the Multiplexer |
| InterpreterValueError | | |
| InterpreterConversionError | an invalid conversion took place | |
| InterpreterRuntimeError | a general runtime exception | |
| InterpreterInstructionError | an instruction is encountered that is not valid | an invalid instruction xyz is encountered |

