from instructions import Instructions


class AsmDoc:

    tags = {"@brief" : "", "@param" : "", "@return" : "", "@post" : "", "@note" : ""}

    label_tips = {
    }

    instr_tip = {
        "add" : ["add",            "add $t1, $t2, $t3",   "$t1 = $t2 + $t3",    "addition"],
        "sub" : ["subtract",       "sub $t1, $t2, $t3",   "$t1 = $t2 - $t3",    "subtraction"],
        "li"  : ["load immediate", "li $t1, 100",         "$t1 = 100",          "Pseudo-instruction (provided by assembler, not processor!) \nLoads immediate value into register"],
        "j"   : ["jump",           "j 1000",                                    "go to address 1000", "jump to target address"],
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
            tip_li = [tip.replace("#", "").strip() for tip in tip]

            formatted_list = [
                f"@brief {line[8:]}" for line in tip_li if line.startswith('@brief')
            ] + [
                f"@note {line[7:]}" for line in tip_li if line.startswith('@note')
            ] + [
                f"@post {line[7:]}" for line in tip_li if line.startswith('@post')
            ] + [
                f"@param {line.split()[1]} {line.split(maxsplit=2)[2]}" for line in tip_li if line.startswith('@param')
            ] + [
                f"@return {line[9:]}" for line in tip_li if line.startswith('@return')
                ]

            fmt_tip = "\n\n".join(formatted_list)

        if word in Instructions.get_all_instructions():
            tip =  self.instr_tip.get(word, "")
            fmt_tip = f"{tip[0]} \n\nExample: {tip[1]} \n\nMeaning: {tip[2]} \n\n{tip[3]}"

        return fmt_tip
