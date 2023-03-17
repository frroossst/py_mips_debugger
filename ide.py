# GUI imports
from PyQt5.QtGui import QTextBlockFormat, QIcon
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QMenuBar, QAction, QFileDialog, QSplitter
from PyQt5.QtCore import Qt, QTimer

# Runtime imports
from instructions import Instructions
from interpreter import Interpreter
from registers import Registers
import breakpoints


class IDE(QWidget):

    filename = None
    last_added_breakpoint = None

    R = None
    I = None

    register_box = None

    def __init__(self, filename):
        self.filename = filename
        super().__init__()
        self.initUI()
        self.setMinimumSize(720, 480)

    def initUI(self):
        self.setWindowTitle("PyMIPS Emulator")
        self.setWindowIcon(QIcon('./assets/icon.png'))

        # Create the QTextEdit widget to display the file contents
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)

        # Registers Window
        self.register_box = QTextEdit(self)
        self.register_box.setReadOnly(True)
        self.register_box.setText("Registers:\n" + self.R.__str__())

        # Create a layout for the window and add the QTextEdit widget to it
        layout = QVBoxLayout()
        btn_hlayout = QHBoxLayout()
        main_hlayout = QSplitter(Qt.Horizontal)
        menu_bar = QMenuBar()

        # Constructing the menu bar
        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

        # Create RUN button
        run_button = QPushButton("RUN", self)
        run_button.clicked.connect(self.runCode)
        btn_hlayout.addWidget(run_button)

        main_hlayout.addWidget(self.register_box)
        main_hlayout.addWidget(self.textEdit)
        main_hlayout.setSizes([200, 500])

        layout.addWidget(menu_bar)
        layout.addWidget(main_hlayout, 2)
        layout.addLayout(btn_hlayout)

        self.setLayout(layout)

        timer = QTimer(self)
        timer.setInterval(500)
        timer.timeout.connect(self.updateRegistersGUI)
        timer.start()
        

        # Load the file and display its contents
        self.loadFile()

        # Connect the cursor position changed signal to the onCursorPositionChanged method
        self.textEdit.mouseDoubleClickEvent = self.onMouseDoubleClickEvent

        self.setup_runtime()

    def setup_runtime(self):
        self.R = Registers()
        self.I = Interpreter(self.filename, self.R)
        self.I.process()
        self.register_box.setText("Registers:\n" + self.R.__str__())

    def loadFile(self):
        # Open the file and read its contents
        with open(self.filename, 'r') as file:
            text = file.read()

        # Add line numbers to the text
        lines = text.split('\n')
        numberedText = '\n'.join([f'{i+1}: {line}' for i, line in enumerate(lines)])

        # Set the text of the QTextEdit widget to the numbered text
        self.textEdit.setText(numberedText)

    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Assembly Files (*.asm, *.s); All Files (*)")

        file_path, _ = file_dialog.getOpenFileName(self, "Open file", "", "Assembly Files (*.asm, *.s); All Files (*)")

        self.filename = file_path
        self.loadFile()


    def onMouseDoubleClickEvent(self, _event):
        # Get the current line number
        cursor = self.textEdit.textCursor()
        block = cursor.block()

        lineNumber = cursor.blockNumber() + 1
        lineText = block.text()

        removing_breakpoint = False

        try:
            _ = breakpoints.GLOBAL_BREAKPOINTS[lineNumber]
            removing_breakpoint = True

            fmt = QTextBlockFormat()
            fmt.setBackground(Qt.white)

            cursor.setBlockFormat(fmt)
        except KeyError:
            breakpoints.GLOBAL_BREAKPOINTS[lineNumber] = lineText
            try:
                extracted_instruction = lineText.split(" ")[5] 
                if extracted_instruction in Instructions.get_all_instructions() and not Instructions.isLabel(breakpoints.consume_line_number_and_return_line(lineText)): 
                    fmt = QTextBlockFormat()
                    fmt.setBackground(Qt.red)

                    cursor.setBlockFormat(fmt)
            except Exception:
                pass
        finally:
            breakpoints.process_and_clean_breakpoints()
            breakpoints.map_ide_breakpoints_to_interpreter_breakpoints(self.textEdit.toPlainText().splitlines(), removing_breakpoint)

            if removing_breakpoint: # removing early to ensure that map_ide_breakpoints_to_interpreter_breakpoints works correctly
                breakpoints.GLOBAL_BREAKPOINTS.pop(lineNumber)

        print(f"Breakpoints: {breakpoints.GLOBAL_BREAKPOINTS}")
        print(f"Interpreted breakpoints: {breakpoints.INTERPRETED_BREAKPOINTS}")

    def runCode(self):
        self.I.run()

    def updateRegistersGUI(self):
        # Get the current scroll position
        scroll_bar = self.register_box.verticalScrollBar()
        scroll_pos = scroll_bar.value()

        self.register_box.setText(self.R.__str__())

        # Restore the scroll position
        scroll_bar.setValue(scroll_pos)

