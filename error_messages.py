from fuzzy_match import get_closest_match_from_list

class ErrorMessages:

    def __init__(self):
        pass

    @classmethod    
    def consider_replacing_with_valid_register(self):
        return "Consider replacing it with a valid register like: $t0, $s0, $v0 etc."

    @classmethod
    def consider_replacing_with_valid_label(self, m, label):
        return get_closest_match_from_list(f"Did you mean {get_closest_match_from_list(label, m.get_memory_keys())} instead?")

    @classmethod
    def get_error_message_where_move_register_is_invalid(self, r, m, instr, invalid_arg):
        return f"{instr} takes in two registers as arguments, {invalid_arg} is not a valid register" + "\n" + self.consider_replacing_with_valid_register()

    @classmethod
    def get_error_message_where_label_is_invalid(self, r, m, inst, invalid_arg):
        return f"{inst} takes in a label as an argument, {invalid_arg} is not a valid label" + "\n" + self.consider_replacing_with_valid_label(m, invalid_arg)

    @classmethod
    def get_error_message_li_where_register_is_invalid(self, invalid_arg):
        return f"li takes in a register and an integer as arguments, {invalid_arg} is not a valid register" + "\n" + self.consider_replacing_with_valid_register()

    @classmethod
    def get_error_message_li_where_integer_is_invalid(self, invalid_arg):
        return f"li takes in a register and an integer as arguments, {invalid_arg} is not a valid integer"



