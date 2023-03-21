from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter

class MIPSHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(MIPSHighlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkBlue)
        keywordFormat.setFontWeight(QFont.Bold)

        registerFormat = QTextCharFormat()
        registerFormat.setForeground(Qt.darkGreen)

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(Qt.gray)

        instructionList = ["add", "addi", "sub", "and", "or", "nor", "slt", "lw", "sw", "beq", "j", "jal", "jr"]
        self.highlightingRules = [(QRegExp("\\b%s\\b" % word), keywordFormat) for word in instructionList]
        self.highlightingRules += [(QRegExp("\\$[a-z]+\\d"), registerFormat)]
        self.highlightingRules.append((QRegExp("#[^\n]*"), commentFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)