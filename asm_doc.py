class AsmDoc:

    label_tips = {}
    instr_tip = {
       "main" : "main entry point", 
    }

    @classmethod
    def generate_asm_doc(self, text):
        pass

    @classmethod
    # create a dictionary of labels and their accompanied javadoc comments
    def get_asm_doc(self, word):
        return self.instr_tip["main"]
        # return self.label_tips.get(word, None)