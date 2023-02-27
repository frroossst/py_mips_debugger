from multiplexer import Multiplexer

class Interpreter:

    file_name = ""
    text = ""
    data = ""
    registers_ref = None

    def __init__(self, file_name, r):
        self.registers_ref = r
        self.file_name = file_name
        with open(file_name, 'r') as f:
            content = f.readlines()
            # find .text heading and put everything after it in text
            for i in range(len(content)):
                if content[i].strip() == ".text":
                    self.text = content[i + 1:]
                    break
        if self.text == "":
            raise ValueError("No .text section found in file")
        else:
            self.text = [ x.strip() for x in "".join(self.text).splitlines() if x.strip() != "" ]

    def run(self):
        print(self.text)
        Multiplexer.decode_instruction(self.registers_ref, "li", "$t1, 52".split(", "))


