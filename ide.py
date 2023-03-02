from PyQt5.QtGui import QTextBlockFormat, QTextCursor, QTextCharFormat, QTextDocument, QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QEvent, QRectF, QPointF, QSize
from instructions import Instructions
from interpreter import Interpreter
import breakpoints
import sys


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
            _ = breakpoints.GLOBAL_BREAKPOINTS[lineNumber]
            breakpoints.GLOBAL_BREAKPOINTS.pop(lineNumber)

            fmt = QTextBlockFormat()
            fmt.setBackground(Qt.white)

            cursor.setBlockFormat(fmt)
        except KeyError:
            breakpoints.GLOBAL_BREAKPOINTS[lineNumber] = lineText
            try:
                extracted_instruction = lineText.split(" ")[5] 
                if extracted_instruction in Instructions.get_all_instructions() and not Instructions.isLabel(lineText): 
                    fmt = QTextBlockFormat()
                    fmt.setBackground(Qt.red)

                    cursor.setBlockFormat(fmt)
            except Exception as e:
                pass
        finally:
            breakpoints.process_and_clean_breakpoints()
            breakpoints.map_ide_breakpoints_to_interpreter_breakpoints(self.textEdit.toPlainText().splitlines())

        print(f"Breakpoints: {breakpoints.GLOBAL_BREAKPOINTS}")

