[![pages-build-deployment](https://github.com/frroossst/py_mips_debugger/actions/workflows/pages/pages-build-deployment/badge.svg?branch=master)](https://github.com/frroossst/py_mips_debugger/actions/workflows/pages/pages-build-deployment)

# Installation and Usage

## Prerequisites
- have python >= 3.10 installed
- have access to the pip python manager (or install the dependencies from requirements.txt)

## Installation

`pip3 install -r requirements.txt`  
> NOTE: some installation will require you to use `pip` instead of `pip3`  



`make build`  

this build an executable for your platform be it linux, windows or macOS, an executable will be created in dist/ subdirectory, simply run that executable from the terminal with the path to your assembly file as an argument.  


`./PyMIPS hello.asm`  
`<path to executable> <path to asm file>`

# Goals

- A minimal MIPS interpreter in Python, (usask's CMPT 215 as a reference for what is supported)
- Less than 5 megabyte
- Make debugging easier
- Ensure compatibility with VSCode using the inbuilt Python DAP
- Reinvent parts of the wheel as needed, rather than the whole
- Minimal installation and dependencies, tiny executable

# Limitations

These limitations primarily stem from, my laziness and the goal of the project to provide support for a minimal 
subset of the MIPS Assembly Instruction set, this means that while most instructions are supported and this subset is
intended to be Turing complete all behaviours might not work for an officially supported assembler or emulator.

- You NEED to have a main label else the program will throw an error
- Nested labels are not supported
```
    foo:
        bar:
            # This is not supported
```
- Dropdown label execution is not supported
```
foo:
    # instructions

bar:
    # instructions

main:
    j foo

# execution flow for dropdown(s)
# main -> foo -> bar

# when dropdown(s) aren't supported
# main -> foo
# each label has sort of an "end label" tag
# and so when it is hit, the execution is returned or ended
# depending on what instruction was used
```
