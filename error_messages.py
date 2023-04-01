class ErrorMessages:

    def __init__(self):
        pass

    @classmethod    
    def consider_replacing_with_valid_register(self):
        return "Consider replacing it with a valid register like: $t0, $s0, $v0 etc."

    @classmethod
    def consider_replacing_with_valid_label(self):
        return "Consider replacing it with a valid label like: loop, main, start etc. You can see all the vallid labels in the Memory tab of the IDE"

    @classmethod
    def get_error_message_where_move_register_is_invalid(self, instr, invalid_arg):
        return f"{instr} takes in two registers as arguments, {invalid_arg} is not a valid register" + "\n" + self.consider_replacing_with_valid_register()

    @classmethod
    def get_error_message_where_label_is_invalid(self, inst, invalid_arg):
        return f"{inst} takes in a label as an argument, {invalid_arg} is not a valid label" + "\n" + self.consider_replacing_with_valid_register()

    @classmethod
    def get_error_message_li_where_register_is_invalid(self, invalid_arg):
        return f"li takes in a register and an integer as arguments, {invalid_arg} is not a valid register" + "\n" + self.consider_replacing_with_valid_register()

    @classmethod
    def get_error_message_li_where_integer_is_invalid(self, invalid_arg):
        return f"li takes in a register and an integer as arguments, {invalid_arg} is not a valid integer"



