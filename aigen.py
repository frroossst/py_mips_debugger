from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QToolTip
from PyQt5.QtCore import Qt
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create left QTextEdit widget
        self.left_textedit = QTextEdit(self)
        self.left_textedit.setGeometry(10, 10, 300, 400)
        self.left_textedit.setMouseTracking(True)
        self.left_textedit.mouseMoveEvent = self.left_textedit_mouse_move

        # Create right QTextEdit widget
        self.right_textedit = QTextEdit(self)
        self.right_textedit.setGeometry(320, 10, 300, 400)

    def left_textedit_mouse_move(self, event):
        # Get the current cursor position
        cursor = self.left_textedit.cursorForPosition(event.pos())

        # Get the line number of the current cursor position
        line_number = cursor.blockNumber()

        # Get the text of the current line
        line_text = cursor.block().text()

        # Generate a random number between 1 and 100
        random_number = random.randint(1, 100)

        # Set the tooltip with the random number for the current line
        QToolTip.showText(event.globalPos(), f"{line_text.strip()} : {random_number}")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

