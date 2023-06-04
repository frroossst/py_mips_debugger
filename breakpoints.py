from better_data_structures import better_deque
from instructions import Instructions
import queue

GLOBAL_BREAKPOINTS = {}
INTERPRETED_BREAKPOINTS = {}
STOP_AT_NEXT_INSTRUCTION = False
MESSAGE_QUEUE = queue.Queue()
BUTTON_STACK = better_deque()
WATCHED_EXPRESSIONS = []
EVALUATED_WATCHED_EXPRESSIONS = {}
CURRENT_EXECUTING_OBJECT = {}


def subscribe_currently_executing_object(label, index, instr):
    CURRENT_EXECUTING_OBJECT["label"] = label
    CURRENT_EXECUTING_OBJECT["index"] = index
    CURRENT_EXECUTING_OBJECT["instr"] = instr

def consume_line_number_and_return_line(line):
    for x, i in enumerate(line):
        if i.isnumeric() or i == ":":
            continue
        else:
            return line[x:]

def return_line_number_from_GUI_instruction_line(line):
    for x, i in enumerate(line):
        if i.isnumeric() or i == ":":
            continue
        else:
            return int(line[:x - 1])

def get_line_number_from_label_index(text, label, index):
    lines = text.splitlines()

    last_label = None
    count_from_label = 0
    for x, i in enumerate(lines):
        line_number_from_instruction = return_line_number_from_GUI_instruction_line(i)
        fmt_line = consume_line_number_and_return_line(i).strip()
        if Instructions.isLabel(fmt_line):
            fmt_line = fmt_line[0:-1].strip() # remove colon and whitespace
            last_label = fmt_line
            count_from_label = 0
            continue

        if fmt_line == "":
            continue

        if fmt_line.startswith("#"):
            continue

        if (label == last_label) and (index == count_from_label):
            return line_number_from_instruction

        count_from_label += 1

    return None

def remove_duplicate_breakpoints():
    # remove duplicate values in the list
    for k, v in INTERPRETED_BREAKPOINTS.items():
        INTERPRETED_BREAKPOINTS[k] = list(set(v))

def map_ide_breakpoints_to_interpreter_breakpoints(text_list, removing_breakpoints, quiet=False):
    for k, v in GLOBAL_BREAKPOINTS.items():
        last_label = None
        label_offset = 0
        for x, i in enumerate(text_list):
            label_offset += 1
            if Instructions.isLabel(consume_line_number_and_return_line(i)):
                last_label = i.split(":")[1].strip()
                label_offset = 0
            elif consume_line_number_and_return_line(i).strip().startswith("#") or consume_line_number_and_return_line(i).strip() == "":
                label_offset -= 1
                continue
            elif v.split(":")[1].strip() == i.split(":")[1].strip():
                # print(f"Found breakpoint at IDE line {k} in label {last_label} and is instruction number {label_offset}")
                # TODO: remove breakpoints too at some time
                if (last_label is not None) and (last_label not in list(INTERPRETED_BREAKPOINTS.keys())):
                    INTERPRETED_BREAKPOINTS[last_label] = [label_offset - 1]
                    break
                else:
                    if (not removing_breakpoints) and (not Instructions.isDirective(consume_line_number_and_return_line(i))):
                        INTERPRETED_BREAKPOINTS[last_label].append(label_offset - 1)
                        remove_duplicate_breakpoints()
                    elif (last_label is not None):
                        print(INTERPRETED_BREAKPOINTS)
                        print("removed breakpoint: ", v)
                        print("from label: ", last_label)
                        print("at instruction number: ", label_offset - 1)
                        val = INTERPRETED_BREAKPOINTS[last_label]
                        val.remove(label_offset - 1)
                        INTERPRETED_BREAKPOINTS[last_label] = val
                        remove_duplicate_breakpoints()
                        return None


def process_and_clean_breakpoints():
        # remove all breakpoints that are not instructions
    for k, v in GLOBAL_BREAKPOINTS.copy().items():
        # removing labels
        if Instructions.isLabel(v.split(" ")[1]):
            GLOBAL_BREAKPOINTS.pop(k)
        # remove empty lines
        elif v.strip()[-1] == ":" and v.split(":")[0].isnumeric():
            GLOBAL_BREAKPOINTS.pop(k)
        # remove comments
        elif v.split(":")[1].strip()[0] == "#":
            GLOBAL_BREAKPOINTS.pop(k) 
        # remove directives
        elif Instructions.isDirective(v.split(":")[1].strip()):
            GLOBAL_BREAKPOINTS.pop(k)

def evaluate_watched_expressions(registers_ref):
    EVALUATED_WATCHED_EXPRESSIONS = {}
    for i in WATCHED_EXPRESSIONS:
        # get source register value
        source_value = registers_ref.get_register(i["register_source"])

        # check if target is a register or a numeric literal
        target_value = i["register_target"]
        if registers_ref.get_register_validity(i["register_target"]):
            target_value = registers_ref.get_register_value(i["register_target"])

        eval_str = str(source_value) + " " + i["operator"] + " " + str(target_value)
        eval_val = eval(eval_str)

        EVALUATED_WATCHED_EXPRESSIONS[f"{i['register_source']} {i['operator']} {i['register_target']}"] = eval_val

def add_watch_expression(src, op, target):
    watch_object = {"register_source": src, "register_target": target, "operator": op}
    WATCHED_EXPRESSIONS.append(watch_object)

def remove_watch_expression(expression):
    li = expression.split(" ")
    src, op, target = li[0], li[1], li[2]
    watch_object = {"register_source": src, "register_target": target, "operator": op}
    WATCHED_EXPRESSIONS.remove(watch_object)
