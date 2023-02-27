from instructions import Instuctions

class Multiplexer:

    def decode_and_execute(r, ins, args):
        if ins == "li":
            Instuctions.li(r, args[0].strip(","), args[1])
