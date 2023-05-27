[![.github/workflows/py_unit_test.yml](https://github.com/frroossst/py_mips_debugger/actions/workflows/py_unit_test.yml/badge.svg)](https://github.com/frroossst/py_mips_debugger/actions/workflows/py_unit_test.yml)
[![pages-build-deployment](https://github.com/frroossst/py_mips_debugger/actions/workflows/pages/pages-build-deployment/badge.svg?branch=master)](https://github.com/frroossst/py_mips_debugger/actions/workflows/pages/pages-build-deployment)
![GitHub issues](https://img.shields.io/github/issues-raw/frroossst/py_mips_debugger?style=plastic)

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

- [ ] A minimal MIPS interpreter in Python, (usask's CMPT 215 as a reference for what is supported)
- [x] Make debugging MIPS assembly easier
- [ ] Minimal dependencies
    - toml
    - PyQt5
    - termcolor
- [x] Easy to install
- [ ] Tiny executable
    - 86.4 MB (large due to statically linking PyQt5)
- ~Ensure compatibility with VSCode using the inbuilt Python DAP~   
    - [x] Implemented custom debugging interface   

# Guiding Philosophy
- Reinvent parts of the wheel as needed, rather than the whole

# Design Choices

These limitations primarily stem from, my laziness and the goal of the project to provide support for a minimal 
subset of the MIPS Assembly Instruction set, this means that while most instructions are supported and this subset is
intended to be Turing complete, all behaviours might not exactly replicate an officially supported assembler or emulator.

- You NEED to have a main label else the program will throw an error
- Nested labels are not supported
```
    foo:
        bar:
            # This is not supported
```
