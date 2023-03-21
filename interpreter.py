from PyQt5.QtCore import QCoreApplication, QObject, pyqtSignal

from exceptions import InterpreterSyntaxError, InterpreterProcessError, InterpreterRecursionError
from helper_instructions import EndOfInstruction
from instructions import Instructions
from multiplexer import Multiplexer
from collections import OrderedDict
import breakpoints

class Interpreter(QObject):

    highlight_line = pyqtSignal(dict)

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

    step_button_pressed = False
    continue_button_pressed = False
    state_of_step = False


    def __init__(self, file_name, r):
        super().__init__()

        self.file_name = file_name
        self.text, self.data = "", ""

        self.labels, self.label_index = OrderedDict(), {}

        self.registers_ref, self.__breakpoints__, self.__call_stack__ = r, {}, []

        self.__processed__, self.__foundmain__ = False, False

        self.step_button_pressed, self.continue_button_pressed, self.state_of_step = False, False, False

        with open(file_name, 'r') as fobj:
            content = fobj.readlines()
            # find .text heading and put everything after it in text
            for i in range(len(content)):
                if content[i].strip() == ".text":
                    self.text = content[i + 1:]
                    self.text_starts_at_line = i + 1
                    break

        if self.text == "":
            raise InterpreterSyntaxError("No .text section found in file")

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
                    raise InterpreterSyntaxError("Instruction found before label")

        if last_label is not None:
            val = self.labels[last_label]
            val += EndOfInstruction().__str__()
            self.labels[last_label] = val

        if not self.__foundmain__:
            raise InterpreterSyntaxError("No main label found")

        print(self.label_index)
        print(self.labels)

        self.__processed__ = True

    def run(self):
        if not self.__processed__:
            raise InterpreterProcessError("You must call process() before run()")

        # main entry point
        self.execute_label("main")

    def check_and_breakpoint(self, label, instruction_number, check_for_breakpoint=True, quiet=False):
        if check_for_breakpoint:
            while (label in list(breakpoints.INTERPRETED_BREAKPOINTS.keys()) and instruction_number in breakpoints.INTERPRETED_BREAKPOINTS[label]):
                print("Breakpoint hit")
                QCoreApplication.processEvents() # process events to allow the GUI to update and not freeze
                if (self.step_button_pressed or self.continue_button_pressed):
                    self.continue_button_pressed = False
                    # from stop to continue         => want to break
                    # from run  to wanting  to stop => want to NOT break
                    if breakpoints.BUTTON_STACK.get_len() >= 2: # 2 because we want to check the previous button
                        breakpoints.BUTTON_STACK.pop()
                        prev_button = breakpoints.BUTTON_STACK.pop()
                        if prev_button == "step":
                            continue

                    break

        else:
            if breakpoints.STOP_AT_NEXT_INSTRUCTION:
                breakpoints.STOP_AT_NEXT_INSTRUCTION = False
                while (True and not self.continue_button_pressed):
                    QCoreApplication.processEvents() # process events to allow the GUI to update and not freeze
                    print("Step hit")
                    if (self.step_button_pressed and breakpoints.STOP_AT_NEXT_INSTRUCTION):
                        self.step_button_pressed = False
                        self.state_of_step = False
                        break
                
                self.state_of_step = True

    def get_currently_executing_instruction(self):
        try:
            return {
                "label": self.__current_label__,
                "instruction_index": self.__current_instruction_index__,
                "instruction": self.__current_instruction__
            }
        except AttributeError:
            return None

    def execute_label(self, label_to_run, return_control=False):
        try:
            code = self.labels[label_to_run].strip().splitlines()
            for x, i in enumerate(code): 
                print(f"running [{i}] at index {x} in '{label_to_run}'")

                # setting class variables for debugging purposes
                breakpoints.CURRENT_EXECUTING_OBJECT["label"] = label_to_run
                breakpoints.CURRENT_EXECUTING_OBJECT["index"] = x
                breakpoints.CURRENT_EXECUTING_OBJECT["instr"] = i

                self.highlight_line.emit(breakpoints.CURRENT_EXECUTING_OBJECT)

                # checks for breakpoints 
                self.check_and_breakpoint(label_to_run, x, check_for_breakpoint=True, quiet=False)

                instruction = i.split(" ")
                if Multiplexer.reached_end_of_instruction(instruction[0]):
                    return None
                if Multiplexer.is_a_jump_instruction(instruction[0]):
                    Multiplexer.process_jump_instruction(self.registers_ref, instruction[0], instruction[1:])
                    if self.registers_ref.ra in list(self.labels):
                        self.execute_label(instruction[1], return_control=True)
                # elif is a branch beq t0, t1, main

                Multiplexer.decode_and_execute(self.registers_ref, instruction[0], instruction[1:])

                # checks for steps
                self.check_and_breakpoint(label_to_run, x, check_for_breakpoint=False, quiet=False)

        except RecursionError:
            raise InterpreterRecursionError("Recursion limit reached", label_that_crashed=label_to_run, instruction_that_crashed=code[x+1])

