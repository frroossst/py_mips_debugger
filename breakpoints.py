from better_data_structures import better_deque
from instructions import Instructions
import queue

GLOBAL_BREAKPOINTS = {}
INTERPRETED_BREAKPOINTS = {}
STOP_AT_NEXT_INSTRUCTION = False
MESSAGE_QUEUE = queue.Queue()
BUTTON_STACK = better_deque()


def consume_line_number_and_return_line(line):
    for x, i in enumerate(line):
        if i.isnumeric() or i == ":":
            continue
        else:
            return line[x:]

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
            elif v.split(":")[1].strip() == i.split(":")[1].strip():
                # print(f"Found breakpoint at IDE line {k} in label {last_label} and is instruction number {label_offset}")
                # TODO: remove breakpoints too at some time
                if last_label not in list(INTERPRETED_BREAKPOINTS.keys()):
                    INTERPRETED_BREAKPOINTS[last_label] = [label_offset - 1]
                    break
                else:
                    if not removing_breakpoints:
                        INTERPRETED_BREAKPOINTS[last_label].append(label_offset - 1)
                        remove_duplicate_breakpoints()
                    else:
                        # INTERPRETED_BREAKPOINTS[last_label].remove(label_offset - 1)
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
