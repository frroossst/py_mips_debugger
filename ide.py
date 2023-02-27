from PyQt5.QtGui import QTextBlockFormat, QTextCursor, QTextCharFormat, QTextDocument, QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QEvent, QRectF, QPointF, QSize
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

    breakpoints = {}
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

        # Connect the cursor position changed signal to the onCursorPositionChanged method
        self.textEdit.cursorPositionChanged.connect(self.onCursorPositionChanged)

        # Create a layout for the window and add the QTextEdit widget to it
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

        # Connect the cursor position changed signal to the onCursorPositionChanged method
        self.textEdit.cursorPositionChanged.connect(self.onCursorPositionChanged)

        # Add a breakpoint icon to the left margin when a line is clicked
        self.textEdit.installEventFilter(self)

        # Load the file and display its contents
        self.loadFile()

    def loadFile(self):
        # Open the file and read its contents
        with open(self.filename, 'r') as file:
            text = file.read()

        # Add line numbers to the text
        lines = text.split('\n')
        numberedText = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(lines)])

        # Set the text of the QTextEdit widget to the numbered text
        self.textEdit.setText(numberedText)

    def onCursorPositionChanged(self):
        # Get the current line number
        cursor = self.textEdit.textCursor()
        block = cursor.block()

        lineNumber = cursor.blockNumber() + 1
        lineText = block.text()

        # Print the line number to the console

        print("---------------------------------")
        print(list(self.breakpoints.keys()))
        print(self.last_added_breakpoint)
        print("---------------------------------")

        if lineNumber in self.breakpoints.keys() and lineNumber != self.last_added_breakpoint:
            print("removing breakpoint")
            print(f'Clicked line: {lineNumber}: {lineText}')

            # clear highlight
            no_highlight_format = QTextBlockFormat()
            no_highlight_format.setBackground(Qt.white)
            cursor.setBlockFormat(no_highlight_format)

            self.breakpoints.pop(lineNumber, None)
            self.last_added_breakpoint = lineNumber

        else:
            print("adding breakpoint")
            print(f'Clicked line: {lineNumber}: {lineText}')

            yellow_highlight_format = QTextBlockFormat()
            yellow_highlight_format.setBackground(Qt.yellow)
            cursor.setBlockFormat(yellow_highlight_format)

            self.breakpoints[lineNumber] = lineText
            self.last_added_breakpoint = lineNumber



    def eventFilter(self, object, event) :
        # Add a breakpoint icon to the left margin when a line is clicked
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                cursor = self.textEdit.cursorForPosition(event.pos())
                block = cursor.block()
                lineNumber = block.blockNumber() + 1

                # Add the breakpoint icon to the left margin
                format = QTextBlockFormat()
                format.setLeftMargin(16)
                block.setBlockFormat(format)

                breakpoint = Breakpoint()
                breakpoint.setObjectName('breakpoint')
                breakpoint.setToolTip(f'Breakpoint on line {lineNumber}')
                breakpoint.setProperty('lineNumber', lineNumber)

                layout = QHBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.addWidget(breakpoint)
                widget = QWidget()
                widget.setLayout(layout)

                self.textEdit.setViewportMargins(16, 0, 0, 0)

                self.textEdit.setLineWrapMode(QTextEdit.NoWrap)
                self.textEdit.setReadOnly(False)
                self.textEdit.setMaximumBlockCount(100000)
                self.textEdit.setDocument(QTextDocument(self))


                leftMargin = QWidget(self.textEdit)
                leftMargin.setObjectName('leftMargin')
                leftMargin.setGeometry(0, 0, 16, 16 * self.textEdit.blockCount())
                self.textEdit.setViewportMargins(16, 0, 0, 0)

                self.updateLeftMargin()

                self.textEdit.installEventFilter(self)

                self.show()

        return super().eventFilter(object, event)

    def updateLeftMargin(self):
        leftMargin = self.textEdit.findChild(QWidget, 'leftMargin')
        if leftMargin is None:
            return
    
        for i in range(self.textEdit.blockCount()):
            block = self.textEdit.document().findBlockByNumber(i)
            breakpoint = leftMargin.findChild(QLabel, f'breakpoint_{i}')
            if breakpoint is None:
                continue
            
            breakpoint.move(0, self.textEdit.cursorRect(block.position()).top())
    
    def paintEvent(self, event):
        painter = QPainter(self)
    
        leftMargin = self.textEdit.findChild(QWidget, 'leftMargin')
        if leftMargin is None:
            return
    
        for i in range(self.textEdit.blockCount()):
            block = self.textEdit.document().findBlockByNumber(i)
            breakpoint = leftMargin.findChild(QLabel, f'breakpoint_{i}')
            if breakpoint is None:
                continue
            
            painter.drawPixmap(0, self.textEdit.cursorRect(block.position()).top(), breakpoint.pixmap())
    
        painter.end()
    


