from PyQt5.QtCore import QCoreApplication, QObject, pyqtSignal

from exceptions import InterpreterSyntaxError, InterpreterProcessError, InterpreterRecursionError, InterpreterRuntimeError, InterpreterValueError
from return_t import BranchShouldNotContinueExecution, EndOfInstructionShouldNotContinueExecution
from helper_instructions import EndOfInstruction
from configuration import Configuration
from instructions import Instructions
from multiplexer import Multiplexer
from collections import OrderedDict
from asm_doc import AsmDoc
import breakpoints

class Interpreter(QObject):

    highlight_line = pyqtSignal(dict)
    rehighlight_signal = pyqtSignal()

    file_name = ""
    text = ""
    data = ""

    labels = OrderedDict()
    label_index = {}

    data_labels = OrderedDict()

    registers_ref = None
    memory_ref    = None
    syscall_ref   = None
    config_ref    = None

    __breakpoints__     = {}
    __call_stack__      = []
    __program_counter__ = None

    __processed__ = False
    __foundmain__ = False

    step_button_pressed = False
    continue_button_pressed = False
    state_of_step = False


    def __init__(self, file_name, r, m, s):
        super().__init__()

        self.file_name = file_name
        self.text, self.data = "", ""

        self.labels, self.label_index, self.data_labels = OrderedDict(), {}, OrderedDict()

        self.registers_ref, self.memory_ref, self.syscall_ref, self.config_ref, self.__breakpoints__, self.__call_stack__ = r, m, s, Configuration(), {}, []

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

            # find .data heading and put everything after it in data but up to the next .text heading
            for i in range(len(content)):
                if content[i].strip() == ".data":
                    for j in range(i + 1, len(content)):
                        if content[j].strip() == ".text":
                            break
                        self.data += content[j]

        if self.text == "":
            raise InterpreterSyntaxError("No .text section found in file")

        self.text = [ x.strip() for x in "".join(self.text).splitlines() if x.strip() != "" ]
        self.data = [ x.strip() for x in "".join(self.data).splitlines() if x.strip() != "" ]

    def process(self):
        last_label = None
        for x, i in enumerate(self.text):
            if Instructions.isLabel(i):
                if i == "main:":
                    self.__foundmain__ = True

                found_colon = False
                for j in i:
                    if j == ":":
                        found_colon = True
                        continue
                    if found_colon and len(j.strip()) > 0:
                            raise InterpreterSyntaxError("Label must be defined on it's own line")

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

                elif i.startswith("#"):
                    continue
                else:
                    raise InterpreterSyntaxError("Instruction found before label")

        if last_label is not None:
            val = self.labels[last_label]
            val += EndOfInstruction().__str__()
            self.labels[last_label] = val

        if not self.__foundmain__:
            raise InterpreterSyntaxError("No main label found")

        AsmDoc.generate_asm_doc(self.text)

        # process .data section
        if self.data != []:
            for i in self.data:
                curr_label = Instructions.extract_label_from_line(i)
                self.data_labels[curr_label] = Instructions.consume_directive_from_line(i[len(curr_label) + 1:].strip())

        self.memory_ref.map_text(self.labels)
        self.memory_ref.map_data(self.data_labels)

        for i in self.labels:
            self.label_index[i] = self.memory_ref.get_address(i)

        self.__processed__ = True

    def run(self):
        if not self.__processed__:
            raise InterpreterProcessError("You must call process() before run()")

        if self.config_ref.get_config("entry_point") != "main":
            self.execute_label(self.config_ref.get_config("entry_point"))
        else:
            # main entry point
            self.execute_label("main")

    def check_and_breakpoint(self, label, instruction_number, check_for_breakpoint=True):
        if check_for_breakpoint:
            while (label in list(breakpoints.INTERPRETED_BREAKPOINTS.keys()) and instruction_number in breakpoints.INTERPRETED_BREAKPOINTS[label]):
                print("Breakpoint hit")
                QCoreApplication.processEvents() # process events to allow the GUI to update and not freeze
                self.rehighlight_signal.emit()
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

            # construct a table of expression and it's truthy value
            breakpoints.evaluate_watched_expressions(self.registers_ref)

        else:
            if breakpoints.STOP_AT_NEXT_INSTRUCTION:
                breakpoints.STOP_AT_NEXT_INSTRUCTION = False
                while (True and not self.continue_button_pressed):
                    QCoreApplication.processEvents() # process events to allow the GUI to update and not freeze
                    self.rehighlight_signal.emit()
                    print("Step hit")
                    if (self.step_button_pressed and breakpoints.STOP_AT_NEXT_INSTRUCTION):
                        self.step_button_pressed = False
                        self.state_of_step = False
                        break
                
                self.state_of_step = True

    def get_next_label(self, curr_label):
        flag = False
        for i in self.labels:
            if i == curr_label:
                flag = True
                continue
            if flag:
                return i
        return None

    def get_currently_executing_instruction(self):
        try:
            return {
                "label": self.__current_label__,
                "instruction_index": self.__current_instruction_index__,
                "instruction": self.__current_instruction__
            }
        except AttributeError:
            return None

    def get_code_from_PC(self):
        for k, v in sorted(self.label_index.items(), key=lambda x: x[1], reverse=True):
            if self.__program_counter__ >= v:
                code = self.labels[k].strip().splitlines()
                offset = (self.__program_counter__ - v) // 4
                code = code[offset:]
                return code

        raise InterpreterValueError("Program Counter is not in any label")

    def get_PC_from_code(self, label, offset):
        offset += 1
        if label in list(self.label_index.keys()):
            return self.memory_ref.get_address(label) + (offset * 4)
        return label + (offset * 4)

    # main interpreter loop
    def execute_label(self, label_to_run):
        try:
            # if label_to_run is a register
            if isinstance(label_to_run, str) and label_to_run[0] == "$":
                label_to_run = self.registers_ref.get_register(label_to_run.strip("$"))
            # if label_to_run is a Progam Counter value, then we need to find the label that contains that PC value
            if isinstance(label_to_run, int) and label_to_run not in list(self.label_index.values()):
                self.__program_counter__ = label_to_run
                code = self.get_code_from_PC()
            # if label_to_run is a label, then we can just run the code
            if isinstance(label_to_run, str) and label_to_run in list(self.labels.keys()):
                code = self.labels[label_to_run].strip().splitlines()

            for x, i in enumerate(code): 
                print(f"running [{i: <16}] at index {x:03} at '{label_to_run}'")

                self.__program_counter__ = self.get_PC_from_code(label_to_run, x)

                # setting class variables for debugging purposes
                breakpoints.CURRENT_EXECUTING_OBJECT["label"] = label_to_run
                breakpoints.CURRENT_EXECUTING_OBJECT["index"] = x
                breakpoints.CURRENT_EXECUTING_OBJECT["instr"] = i

                self.highlight_line.emit(breakpoints.CURRENT_EXECUTING_OBJECT)

                # checks for breakpoints and watch expressions
                self.check_and_breakpoint(label_to_run, x, check_for_breakpoint=True)

                instruction = Instructions.parse_instruction(i)
                Instructions.sanitise_instruction(self.registers_ref, self.memory_ref, instruction)
                if Multiplexer.reached_end_of_instruction(instruction[0]):
                    if not self.config_ref.get_config("end_of_instruction"):
                        next_label = self.get_next_label(label_to_run)
                        if next_label is None:
                            raise InterpreterRuntimeError(f"No valid instruction found at instruction pointer: {self.__program_counter__}")
                        self.execute_label(next_label)
                    return EndOfInstructionShouldNotContinueExecution # continue, if toml config
                if Multiplexer.is_a_jump_instruction(instruction[0]):
                    Multiplexer.process_jump_instruction(self.registers_ref, instruction[0], self.__program_counter__)
                    if instruction[0] == "jr":
                        self.execute_label(self.registers_ref.get_register(instruction[1][1::]))
                    if self.execute_label(instruction[1]) == EndOfInstructionShouldNotContinueExecution:
                        return EndOfInstructionShouldNotContinueExecution
                elif Multiplexer.is_a_branch_instruction(instruction[0]):
                    do_jump = Multiplexer.check_and_evaluate_branch(self.registers_ref, instruction[0], instruction[1:])
                    if do_jump:
                        branch_label = Instructions.consume_comments_and_return_line(" ".join(instruction)).split(" ")[-1]
                        self.execute_label(branch_label)
                        return BranchShouldNotContinueExecution # so, does not come back after a branch
                    continue

                Multiplexer.decode_and_execute(self.registers_ref, self.memory_ref, self.syscall_ref, instruction[0], instruction[1:])

                # checks for steps
                self.check_and_breakpoint(label_to_run, x, check_for_breakpoint=False)

        except RecursionError: 
            raise InterpreterRecursionError("Interpreter Stack Overflow Recursion Limit reached", label_that_crashed=label_to_run, instruction_that_crashed=self.get_code_from_PC()[0])
