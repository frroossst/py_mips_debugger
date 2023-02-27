import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt

class TextEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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

        # Load the file and display its contents
        self.loadFile()

    def loadFile(self):
        # Open the file and read its contents
        with open('./test_cases/basic.asm', 'r') as file:
            text = file.read()

        # Add line numbers to the text
        lines = text.split('\n')
        numberedText = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(lines)])

        # Set the text of the QTextEdit widget to the numbered text
        self.textEdit.setText(numberedText)

    def onCursorPositionChanged(self):
        # Get the current line number
        cursor = self.textEdit.textCursor()
        lineNumber = cursor.blockNumber() + 1

        # Print the line number to the console
        print(f'Clicked line: {lineNumber}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())

