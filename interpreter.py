from instructions import Instructions
from multiplexer import Multiplexer
from collections import OrderedDict
from helper_instructions import *
import breakpoints

class Interpreter:

    file_name = ""
    text = ""
    data = ""

    labels = OrderedDict()
    label_index = {}

    registers_ref = None
    __breakpoints__ = {}
    __call_stack__ = []

    __processed__ = False
    __foundmain__ = False


    def __init__(self, file_name, r):
        self.registers_ref = r
        self.file_name = file_name

        with open(file_name, 'r') as fobj:
            content = fobj.readlines()
            # find .text heading and put everything after it in text
            for i in range(len(content)):
                if content[i].strip() == ".text":
                    self.text = content[i + 1:]
                    self.text_starts_at_line = i + 1
                    break

        if self.text == "":
            raise SyntaxError("No .text section found in file")

        self.text = [ x.strip() for x in "".join(self.text).splitlines() if x.strip() != "" ]

    def process(self):
        last_label = None
        for x, i in enumerate(self.text):
            if Instructions.isLabel(i):
                if i == "main:":
                    self.__foundmain__ = True

                if last_label is not None:
                    val = self.labels[last_label]
                    val += EndOfInstruction().__str__()
                    self.labels[last_label] = val

                last_label = i[:-1:]
            else:
                if last_label is not None:
                    try:
                        val = self.labels[last_label]
                    except KeyError:
                        val = ""
                    finally:
                        # append only if not a comment
                        if not i.startswith("#"):
                            val += i
                            val += "\n"
                        self.labels[last_label] = val

                        if last_label not in list(self.label_index):
                            self.label_index[last_label] = self.text_starts_at_line + x + 1
                else:
                    raise SyntaxError("Instruction found before label")

        if last_label is not None:
            val = self.labels[last_label]
            val += EndOfInstruction().__str__()
            self.labels[last_label] = val

        if not self.__foundmain__:
            raise SyntaxError("No main label found")

        print(self.label_index)
        print(self.labels)

        self.__processed__ = True

    def run(self):
        if not self.__processed__:
            raise ValueError("You must call process() before run()")

        self.execute_label("main")

    def check_and_breakpoint(self, label, instruction_number):
        if label in list(breakpoints.INTERPRETED_BREAKPOINTS.keys()):
            if instruction_number in breakpoints.INTERPRETED_BREAKPOINTS[label]:
                while (True):
                    print("Breakpoint hit")
                    pass

    def execute_label(self, label_to_run, return_control=False):
        # main entry point
        code = self.labels[label_to_run].strip().splitlines()
        for x, i in enumerate(code): 
            self.check_and_breakpoint(label_to_run, x)
            instruction = i.split(" ")
            if Multiplexer.reached_end_of_instruction(instruction[0]):
                return None
            if Multiplexer.is_a_jump_instruction(instruction[0]):
                Multiplexer.process_jump_instruction(self.registers_ref, instruction[0], instruction[1:])
                if self.registers_ref.ra in list(self.labels):
                    self.execute_label(instruction[1], return_control=True)
            # elif is a branch beq t0, t1, main

            Multiplexer.decode_and_execute(self.registers_ref, instruction[0], instruction[1:])
