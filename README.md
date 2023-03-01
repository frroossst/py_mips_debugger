
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