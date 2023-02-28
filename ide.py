from PyQt5.QtGui import QTextBlockFormat, QTextCursor, QTextCharFormat, QTextDocument, QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QEvent, QRectF, QPointF, QSize
from breakpoints import GLOBAL_BREAKPOINTS
from instructions import Instuctions
from interpreter import Interpreter
import sys


class Breakpoint(QLabel):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.setFixedSize(QSize(16, 16))
        self.setAlignment(Qt.AlignCenter)
        self.setPixmap(self.makePixmap())

    def makePixmap(self):
        size = self.size().width()
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.red, 2))
        painter.setBrush(Qt.red)
        painter.drawEllipse(QRectF(2, 2, size - 4, size - 4))
        painter.end()
        return pixmap



class IDE(QWidget):

    filename = None

    last_added_breakpoint = None

    def __init__(self, filename):
        self.filename = filename
        super().__init__()
        self.initUI()
        self.setMinimumSize(720, 480)

    def initUI(self):
        # Create the QTextEdit widget to display the file contents
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)

        # Create a layout for the window and add the QTextEdit widget to it
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

        # Load the file and display its contents
        self.loadFile()

        # Connect the cursor position changed signal to the onCursorPositionChanged method
        self.textEdit.mouseDoubleClickEvent = self.onMouseDoubleClickEvent

    def loadFile(self):
        # Open the file and read its contents
        with open(self.filename, 'r') as file:
            text = file.read()

        # Add line numbers to the text
        lines = text.split('\n')
        numberedText = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(lines)])

        # Set the text of the QTextEdit widget to the numbered text
        self.textEdit.setText(numberedText)

    def onMouseDoubleClickEvent(self, event):
        # Get the current line number
        cursor = self.textEdit.textCursor()
        block = cursor.block()

        lineNumber = cursor.blockNumber() + 1
        lineText = block.text()

        try:
            _ = GLOBAL_BREAKPOINTS[lineNumber]
            GLOBAL_BREAKPOINTS.pop(lineNumber)

            fmt = QTextBlockFormat()
            fmt.setBackground(Qt.white)

            cursor.setBlockFormat(fmt)
        except KeyError:
            GLOBAL_BREAKPOINTS[lineNumber] = lineText

            try:
                extracted_instruction = lineText.split(" ")[5] 
                print(extracted_instruction)
                if extracted_instruction in Instuctions.get_all_instructions() and not Instuctions.isLabel(lineText): 
                    fmt = QTextBlockFormat()
                    fmt.setBackground(Qt.red)

                    cursor.setBlockFormat(fmt)
            except Exception as e:
                pass

        print(f"Breakpoints: {GLOBAL_BREAKPOINTS}")

