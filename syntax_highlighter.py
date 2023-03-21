from PyQt5.QtGui import QTextCharFormat, QFont, QColor, QSyntaxHighlighter
from PyQt5.QtCore import QRegularExpression, QRegularExpressionMatch

class AssemblyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.highlighting_rules = []

        # Define the formatting for keywords
        keyword_format = QTextCharFormat()
        keyword_format.setFontWeight(QFont.Bold)
        keyword_format.setForeground(QColor("#0057e7"))  # Blue color

        # Define the list of assembly language keywords
        keywords = ['addi']

        # Define the regular expression pattern for matching assembly language keywords
        self.keyword_pattern = QRegularExpression("\\b(" + "|".join(keywords) + ")\\b")
        self.keyword_format = keyword_format

    def highlightBlock(self, text):
        # Apply keyword formatting
        match_iterator = self.keyword_pattern.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)

