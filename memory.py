from exceptions import InterpreterMemoryError, InterpreterProcessError
from helper_instructions import EndOfInstruction
from collections import OrderedDict

class Memory:

    memmap = OrderedDict()

    text_addr_start = 40_000
    data_addr_start = 100_000

    text_addr_end = None
    data_addr_end = None

    text_curr_addr = None
    data_curr_addr = None

    is_text_mapped = False
    is_data_mapped = False

    def __init__(self):
        self.memmap = OrderedDict()
        self.is_text_mapped = False
        self.is_data_mapped = False

    def __str__(self) -> str:
        fmt = ""
        keys = sorted((self.memmap.keys()), key=lambda k: (1, k) if isinstance(k, int) else (0, k))  

        label_insert, data_insert = True, True
        for k in keys:
            try:
                int(k)
                if label_insert:
                    fmt += "\n"
                    label_insert = False

                if data_insert and k >= self.data_addr_start:
                    fmt += "\n"
                    data_insert = False
                
                fmt += f"{k}: {self.memmap[k]}\n"
            except ValueError:
                fmt += f"{k}: {self.memmap[k]}\n"

        return fmt

    def map_text(self, text):
        addr = self.text_addr_start

        for i in text:
            self.memmap[i] = addr
            for j in text[i].split("\n"):
                if j == "" or j == EndOfInstruction().__str__().strip():
                    continue
                self.memmap[addr] = j
                addr += 4

        self.is_text_mapped = True

    def map_data(self, data):
        self.data_curr_addr = self.data_addr_start
        starter_ptr = 0

        # data = {directive: value, value: value}

        for i in data:
            val = self.process_directive(data[i]["directive"], data[i]["value"])
            starter_ptr = self.data_curr_addr
            for j in bytes(val, "ascii"):
                self.memmap[self.data_curr_addr] = j
                self.data_curr_addr += 1
            self.memmap[i] = starter_ptr
            
        self.is_data_mapped = True

    def process_directive(self, directive, value):
        if directive == ".asciiz":
            value = value.strip("\"").strip("'") + "\x00"
            byte_string = bytes(value, "ascii").replace(b"\\n", b"\x0A")
            byte_string = byte_string.decode("ascii").strip("\"").strip("'")
            return byte_string

        return value

    def check_bounds(self, addr):
        if (addr < self.data_addr_end and addr >= self.data_addr_start) or (addr < self.text_addr_end and addr >= self.text_addr_start):
            raise InterpreterMemoryError("Memory address out of bounds")

        if addr not in self.memmap.values():
            raise InterpreterMemoryError("Memory address not found")
        
    def get_address(self, label):
        if label not in self.memmap:
            raise InterpreterMemoryError(f"Label {label} not found")

        return self.memmap[label]

    def get_from_memory(self, addr):
        if not (self.is_text_mapped and self.is_data_mapped):
            raise InterpreterProcessError(f"incorrectly mapped memory: text: {self.is_text_mapped}, data: {self.is_data_mapped}")
        self.check_bounds(addr)

    def set_in_memory(self, addr, val):
        if not (self.is_text_mapped and self.is_data_mapped):
            raise InterpreterProcessError(f"incorrectly mapped memory: text: {self.is_text_mapped}, data: {self.is_data_mapped}")
        self.check_bounds(addr)

