# Usage

## Running the emulator
Now you can simply run the main.py file with the path to an assembly file as an argument    
`python3 main.py <path_to_assembly_file>`  

or alterantively you can complile the python files into a c executable binary, this is useful if you want the emulator
to be available as a shell command by moving it to `~/.local/bin` or any other executable path

## Compiling and running the emulator

To compile the emulator, first enssure that you can run the `make` command then simply run,  
`make build`  

this will compile a binary in the `dist/` subdiretory of the project

to run the emulator simply `./dist/PyMIPS <path_to_assembly_file>`

## Configuration file 

The Configuration file is `pymips.toml`

### Features
| key | values | description |
| --- | --- | --- |
| register_base | `bin` `dec` `hex` | the numerical base all registers display in, under the hood it's still decimal |
| memory_mapped | `true` `false` | enable or disable memory mapped registers |
| end_of_instruction | `true` `false` | enable or disable end of instruction |

### Runner
| key | values | description |
| --- | --- | --- |
| entry_point | `label name` | the label which executes at the start of the program |
| file_to_run | `path` | the path to the assembly file to run |

### Debugger
| key | values | description |
| --- | --- | --- |
| breakpoints | `list of line number(s)` | a list of line numbers to break at |
| watchpoints | `list of expression(s)` | a list of expressions to watch |
