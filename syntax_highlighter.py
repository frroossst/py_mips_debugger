from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter

class MIPSHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(MIPSHighlighter, self).__init__(parent)

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(199, 76, 178)) #C74CB2

        registerFormat = QTextCharFormat()
        registerFormat.setForeground(QColor(129, 154, 116)) #819A74

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(Qt.gray)

        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor(233, 124, 68)) #E97C44

        labelFormat = QTextCharFormat()
        labelFormat.setForeground(QColor(248, 221, 93)) #F8DD5D
        labelFormat.setFontWeight(QFont.Bold)

        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor(175, 178, 43)) #AFB22B
        stringFormat.setFontItalic(True)

        directiveFormat = QTextCharFormat()
        directiveFormat.setForeground(QColor(245, 72, 53)) #F54835
        directiveFormat.setFontItalic(True)

        sectionFormat = QTextCharFormat()
        sectionFormat.setForeground(QColor(205, 131, 123)) #CD837B
        sectionFormat.setFontWeight(QFont.Bold)

        todoCommentFormat = QTextCharFormat()
        todoCommentFormat.setForeground(QColor(235, 139, 12)) #EB8B0C
        todoCommentFormat.setFontWeight(QFont.Bold)

        exclaimCommentFormat = QTextCharFormat()
        exclaimCommentFormat.setForeground(Qt.red) 
        exclaimCommentFormat.setFontWeight(QFont.Bold)

        instructions = ["li", "add", "addi", "sub", "and", "or", "nor", "slt", "lw", "sw", "beq", "j", "jal", "jr"]

        self.highlightingRules = [(QRegExp("\\b%s\\b" % word), keywordFormat) for word in instructions]
        self.highlightingRules += [(QRegExp("\\$[a-z]+\\d"), registerFormat)]
        self.highlightingRules += [(QRegExp("\\b[0-9]+\\b"), numberFormat)]
        self.highlightingRules += [(QRegExp("\\b[a-z]+\\b:"), labelFormat)]
        self.highlightingRules += [(QRegExp("\".*\""), stringFormat)]
        self.highlightingRules += [(QRegExp("\\.[a-z]+"), directiveFormat)]
        self.highlightingRules += [(QRegExp("\\.text"), sectionFormat)]
        self.highlightingRules += [(QRegExp("\\.data"), sectionFormat)]
        self.highlightingRules += [(QRegExp("#[^\n]*"), commentFormat)]
        self.highlightingRules += [(QRegExp("^#\\s*!.*"), exclaimCommentFormat)]
        self.highlightingRules.append((QRegExp("^#\\s*TODO:.*"), todoCommentFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)