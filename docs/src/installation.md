# Installation

## Prerequisites

- Have Python 3.10 or higher installed
- Have pip installed

### Installing dependencies

while you are in the root of your project run:  
    `pip3 install -r requirements.txt`

> NOTE: on some installations it is simply pip, while others use pip3

Currently there are only two dependencies:
- `pyQt5`
- `termcolor`

This project could probably do without termcolor but, for now, it is fine as it is. 

### Running the emulator
Now you can simply run the main.py file with the path to an assembly file as an argument    
`python3 main.py <path_to_assembly_file>`  

or alterantively you can complile the python files into a c executable binary, this is useful if you want the emulator
to be available as a shell command by moving it to `~/.local/bin` or any other executable path

### Compiling and running the emulator

To compile the emulator, first enssure that you can run the `make` command then simply run,  
`make build`  

this will compile a binary in the `dist/` subdiretory of the project

to run the emulator simply `./dist/PyMIPS <path_to_assembly_file>`


