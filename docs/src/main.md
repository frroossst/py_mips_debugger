# main.py

This is the main entry point for the entire program

## Taking in arguments

We take in two inputs using the stdlib's argparse module, the first argument is a path to the assembly file that
you want to run, this does not check for the validity of the `.asm` or `.s` file, which is you could conceivably 
load a python file or a simple text file, and only the pre-processor might throw an error, if not then the interpreter
will further downstream. The `--no-gui` arg can be passed to disable the GUI and just run the Interpreter.

## Setting things up

Setup, the IDE and colour palette (dark theme). We also set up an exception hook, this exception hook allows us
to catch our custom defined exceptions in [exceptions.py](./exceptions.md) and catch them to act appropriately, like
catching an exit code or RecursionError. 

This however still allows us to continue on general Python exceptions, which are handled by PyQt.
