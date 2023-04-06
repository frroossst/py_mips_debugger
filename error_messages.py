from fuzzy_match import get_closest_match_from_list

class ErrorMessages:

    def __init__(self):
        pass

    @staticmethod    
    def consider_replacing_with_valid_register(self, r, reg):
        return f"Did you mean {get_closest_match_from_list(reg, r.get_all_registers_as_list())}" 

    @staticmethod
    def consider_replacing_with_valid_label(self, m, label):
        return f"Did you mean {get_closest_match_from_list(label, m.get_memory_keys())} instead?"

    @staticmethod
    def get_error_message_where_move_register_is_invalid(self, r, m, instr, invalid_arg):
        return f"{instr} takes in two registers as arguments, {invalid_arg} is not a valid register" + "\n" + self.consider_replacing_with_valid_register(r, invalid_arg)

    @staticmethod
    def get_error_message_where_label_is_invalid(self, r, m, inst, invalid_arg):
        return f"{inst} takes in a label as an argument, {invalid_arg} is not a valid label" + "\n" + self.consider_replacing_with_valid_label(m, invalid_arg)

    @staticmethod
    def get_error_message_where_memory_address_is_invalid(self, r, m, invalid_arg):
        return f"{invalid_arg} is not a valid memory address" + "\n" + self.consider_replacing_with_valid_label(m, invalid_arg)

