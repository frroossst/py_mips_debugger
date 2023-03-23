from instructions import Instructions


class AsmDoc:

    label_tips = {
    }

    instr_tip = {
        "li" : ["load immediate", "li $t1, 100", "$t1 = 100", "Pseudo-instruction (provided by assembler, not processor!) \nLoads immediate value into register"],

        "j" : ["jump", "j 1000", "go to address 1000", "jump to target address"],
    }

    @classmethod
    def generate_asm_doc(self, text):
        before_label = []
        for i in text:
            if Instructions.isLabel(i):
                self.label_tips[i.strip(":")] = before_label
                before_label = []
            else:
                before_label.append(i)

        # cleanup non-comments
        for k, v in self.label_tips.items():
            self.label_tips[k] = [x for x in v if x.startswith("#")]

        self.label_tips["main"] = "main entry point"

    @classmethod
    def get_asm_doc(self, word):
        tip = self.label_tips.get(word, "")
        if word == "main":
            return tip

        if tip != [] or tip != "":
            fmt_tip = "\n\n".join(tip.replace("#", "") for tip in tip)

        if word in Instructions.get_all_instructions():
            tip =  self.instr_tip.get(word, "")
            fmt_tip = f"{tip[0]} \n\nExample: {tip[1]} \n\nMeaning: {tip[2]} \n\n{tip[3]}"

        return fmt_tip