from exceptions import InterpreterMemoryError, InterpreterProcessError
from collections import OrderedDict

class Memory:

    memmap = OrderedDict()

    text_addr_start = 40_000
    data_addr_start = 100_000

    text_addr_end = None
    data_addr_end = None

    is_text_mapped = False
    is_data_mapped = False

    def __init__(self):
        self.memmap = OrderedDict()
        self.is_text_mapped = False
        self.is_data_mapped = False

    def __str__(self) -> str:
        pass

    def map_text(self, text):
        pass

    def map_data(self, data):
        pass

    def check_bounds(self, addr):
        if (addr < self.data_addr_end and addr >= self.data_addr_start) or (addr < self.text_addr_end and addr >= self.text_addr_start):
            raise InterpreterMemoryError("Memory address out of bounds")

    def get_from_memory(self, addr):
        if not (self.is_text_mapped and self.is_data_mapped):
            raise InterpreterProcessError(f"incorrectly mapped memory: text: {self.is_text_mapped}, data: {self.is_data_mapped}")
        self.check_bounds(addr)

    def set_in_memory(self, addr, val):
        self.check_bounds(addr)

