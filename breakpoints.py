from instructions import Instructions
import queue

GLOBAL_BREAKPOINTS = {}
INTERPRETED_BREAKPOINTS = {'main': [0]}
MESSAGE_QUEUE = queue.Queue()


def consume_line_number_and_return_line(line):
    processed_line = ""
    hit_colon = False
    for x, i in enumerate(line):
        if i.isnumeric():
            continue
        elif i == ":":
            continue
        else:
            return line[x:]

def map_ide_breakpoints_to_interpreter_breakpoints(text_list):
    for k, v in GLOBAL_BREAKPOINTS.items():
        last_label = None
        label_offset = 0
        for x, i in enumerate(text_list):
            print(i)
            label_offset += 1
            if Instructions.isLabel(consume_line_number_and_return_line(i)):
                last_label = i.split(":")[1].strip()
                label_offset = 0
            elif v.split(":")[1].strip() == i.split(":")[1].strip():
                # print(f"Found breakpoint at IDE line {k} in label {last_label} and is instruction number {label_offset}")
                # TODO: remove breakpoints too at some time
                if last_label not in list(INTERPRETED_BREAKPOINTS.keys()):
                    INTERPRETED_BREAKPOINTS[last_label] = [label_offset - 1]
                else:
                    INTERPRETED_BREAKPOINTS[last_label].append(label_offset - 1)
    print(INTERPRETED_BREAKPOINTS)


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
