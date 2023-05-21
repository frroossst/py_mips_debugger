from exceptions import InterpreterMemoryError, InterpreterProcessError
from helper_instructions import EndOfInstruction
from collections import OrderedDict
import struct

class Memory:

    memmap = OrderedDict()

    byte_size     = 1 # bytes
    halfword_size = 2 # bytes
    word_size     = 4 # bytes
    quadword_size = 8 # bytes

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

    def get_memory_keys(self):
        return list(self.memmap.keys())

    def map_text(self, text):
        addr = self.text_addr_start

        for i in text:
            self.memmap[i] = addr
            for j in text[i].split("\n"):
                if j == "" or j == EndOfInstruction().__str__().strip():
                    continue
                self.memmap[addr] = j
                addr += 4

        self.text_addr_end = addr - 4
        self.is_text_mapped = True

    def map_data(self, data):
        self.data_curr_addr = self.data_addr_start

        for i in data:
            val = self.process_directive(data[i]["directive"], data[i]["value"])
            if val["directive"] == "word":
                self.store_new_word(val["value"], i)
            elif val["directive"] == "asciiz" or val["directive"] == "ascii":
                self.store_new_string(val["value"], i)
            elif val["directive"] == "space":
                self.store_new_space(val["value"], i)
            elif val["directive"] == "byte":
                self.store_new_byte(val["value"], i)
            else:
                raise InterpreterProcessError(f"Invalid directive: {val['directive']}")
            
        self.data_addr_end = self.data_curr_addr - 1
        self.data_curr_addr = None
        self.is_data_mapped = True

    def process_directive(self, directive, value):
        if directive == ".asciiz" or directive == ".ascii":
            if directive == ".asciiz":
                value = value.strip("\"").strip("'") + "\x00"
            else:
                value = value.strip("\"").strip("'")
            byte_string = bytes(value, "ascii").replace(b"\\n", b"\x0A")
            byte_string = byte_string.decode("ascii").strip("\"").strip("'")
            return { "directive": "asciiz", "value": byte_string }

        if directive == ".word":
            return { "directive": "word", "value": int(value) }

        if directive == ".space":
            return { "directive": "space", "value": int(value) }

        if directive == ".byte":
            return { "directive": "byte", "value": int(value) }

        return value

    def check_bounds(self, addr, type=None):
        if type == "data":
            if addr > self.data_addr_end and addr < self.data_addr_start:
                raise InterpreterMemoryError(f"Memory address out of bounds: {addr}")
        
        elif type == "text":
            if addr > self.text_addr_end and addr < self.text_addr_start:
                raise InterpreterMemoryError(f"Memory address out of bounds: {addr}")

        elif addr not in self.memmap.keys():
            raise InterpreterMemoryError(f"Memory address not found: {addr}")
        
    def get_address(self, label):
        if label not in self.memmap:
            raise InterpreterMemoryError(f"Label {label} not found")

        return self.memmap[label]

    def get_from_memory(self, addr):
        if not (self.is_text_mapped and self.is_data_mapped):
            raise InterpreterProcessError(f"incorrectly mapped memory: text: {self.is_text_mapped}, data: {self.is_data_mapped}")

        self.check_bounds(addr)
        try:
            val =  self.memmap[addr]
        except KeyError:
            raise InterpreterMemoryError(f"Memory address {addr} not found")

        return val

    def set_in_memory(self, addr, val):
        if not (self.is_text_mapped and self.is_data_mapped):
            raise InterpreterProcessError(f"incorrectly mapped memory: text: {self.is_text_mapped}, data: {self.is_data_mapped}")

        self.check_bounds(addr)
        self.memmap[addr] = val

    def get_char(self, addr):
        self.check_bounds(addr, type="data")

        return chr(self.memmap[addr])

    def get_string(self, addr):
        self.check_bounds(addr, type="data")

        string = ""

        while True:
            if self.memmap[addr] == 0:
                break

            string += chr(self.memmap[addr])
            addr += 1

        return string

    def get_word(self, addr):
        self.check_bounds(addr, type="data")

        word = 0

        for i in range(self.word_size):
            word += self.memmap[addr] << (i * 8)
            addr += 1

        return word

    def store_new_string(self, val, label):
        """
        @note this should not be called directly when executing instructions
        """
        starter_ptr = self.data_curr_addr
        for i in bytes(val, "ascii"):
            self.memmap[self.data_curr_addr] = i
            self.data_curr_addr += 1

        self.memmap[label] = starter_ptr

    def store_new_byte(self, val, label):
        """
        @note this should not be called directly when executing instructions
        """
        starter_ptr = self.data_curr_addr
        self.memmap[self.data_curr_addr] = val
        self.data_curr_addr += 1
        self.memmap[label] = starter_ptr

    def store_new_word(self, val, label):
        """
        @note this should not be called directly when executing instructions
        """
        starter_ptr = self.data_curr_addr

        for _ in range(self.word_size):
            self.memmap[self.data_curr_addr] = val
            self.data_curr_addr += 1

        self.memmap[label] = starter_ptr

    def store_new_space(self, val, label):
        """
        @note this should not be called directly when executing instructions 
        """ 
        starter_ptr = self.data_curr_addr
        for _ in range(val):
            self.memmap[self.data_curr_addr] = 0
            self.data_curr_addr += 1

        self.memmap[label] = starter_ptr

    def store_existing_string(self, val, label):
        starter_ptr = label
        if isinstance(label, str):
            starter_ptr = self.get_address(label)

        for i in bytes(val, "ascii"):
            self.set_in_memory(starter_ptr, i)
            starter_ptr += 1

    def store_existing_word(self, label, val):
        starter_ptr = label
        if isinstance(label, str):
            starter_ptr = self.get_address(label)

        barr = bytearray(val.to_bytes(self.word_size, "little"))

        for i in range(self.word_size):
            self.set_in_memory(starter_ptr, barr[i])
            starter_ptr += 1

    def load_existing_word(self, label):
        starter_ptr = label
        if isinstance(label, str):
            starter_ptr = self.get_address(label)

        li = []

        for _ in range(self.word_size):
            li.append(self.get_from_memory(starter_ptr))
            starter_ptr += 1

        value =  int.from_bytes(bytes(li), "little")
        return value

    def load_existing_unsigned_byte(self, label):
        starter_ptr = label
        if isinstance(label, str):
            starter_ptr = self.get_address(label)

        bytes_li = self.get_from_memory(starter_ptr).to_bytes(1, "little")
        packed   = struct.unpack("B", bytes_li)[0]
        return packed

    def load_existing_byte(self, label):
        starter_ptr = label
        if isinstance(label, str):
            starter_ptr = self.get_address(label)

        bytes_li = self.get_from_memory(starter_ptr).to_bytes(1, "little")
        packed   = struct.unpack("b", bytes_li)[0]
        return packed

