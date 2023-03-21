# GUI imports
from PyQt5.QtGui import QTextBlockFormat, QIcon, QColor, QTextCursor, QTextCharFormat, QFontMetrics, QFont
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QMenuBar, QAction, QFileDialog, QSplitter, QTabWidget, QSizePolicy, QFontDialog
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, QSettings

# Runtime imports
from instructions import Instructions
from interpreter import Interpreter
from registers import Registers
import breakpoints


class IDE(QWidget):

    filename = None
    settings = QSettings("PyMIPS", "PyMIPS Emulator")
    last_added_breakpoint = None

    R = None
    I = None

    register_box = None 
    last_highlighted_line = None

    def __init__(self, filename):
        self.filename = filename
        super().__init__()
        self.initUI()
        self.setMinimumSize(1080, 720)

    def initUI(self):
        self.setWindowTitle("PyMIPS Emulator")
        self.setWindowIcon(QIcon('./assets/icon.png'))

        tab_width = 4 * QFontMetrics(self.font()).width(' ')

        # Create the QTextEdit widget to display the file contents
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.setTabStopWidth(tab_width)

        # Create the QTextEdit widget to edit the file contents
        self.textEditEdit = QTextEdit(self)
        self.textEditEdit.setReadOnly(False)
        self.textEditEdit.setFontPointSize(self.textEdit.fontPointSize() if self.textEdit.fontPointSize() != 0.0 else 10)
        self.textEditEdit.setTabStopWidth(tab_width)

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

        edit_menu = menu_bar.addMenu("Edit")
        font_action = QAction("Font", self)
        font_action.triggered.connect(self.changeFont)
        edit_menu.addAction(font_action)

        # Instructin viewer window
        self.instruction_box = QTextEdit(self)
        self.instruction_box.setReadOnly(True)
        self.instruction_box.setText("Hit RUN to start the emulator")
        self.instruction_box.setMaximumWidth(250)
        self.instruction_box.setMaximumHeight(30)
        self.instruction_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_hlayout.addWidget(self.instruction_box)

        # Create CLEAR button
        clear_button = QPushButton("CLEAR", self)
        clear_button.clicked.connect(self.clearRegisters)
        btn_hlayout.addWidget(clear_button)

        # Create RUN button
        run_button = QPushButton("RUN", self)
        run_button.clicked.connect(self.runCode)
        btn_hlayout.addWidget(run_button)

        # Create STEP button
        step_button = QPushButton("STEP", self)
        step_button.clicked.connect(self.stepCode)
        btn_hlayout.addWidget(step_button)

        # Create CONTINUE button
        continue_button = QPushButton("CONTINUE", self)
        continue_button.clicked.connect(self.continueCode)
        btn_hlayout.addWidget(continue_button)

        # Tabs (view/ edit)
        tab_widget = QTabWidget()
        tab_widget.addTab(self.textEdit, "View")
        tab_widget.addTab(self.textEditEdit, "Edit")
        
        # to save the file when switching tabs
        tab_widget.currentChanged.connect(self.saveFile)

        # Constructing the console window
        self.console = QTextEdit(self)
        self.console.setReadOnly(True)
        self.console.setLineWrapMode(QTextEdit.NoWrap)
        self.console.setAcceptRichText(False)
        self.console.setText("Console:\n")

        main_hlayout.addWidget(self.register_box)
        # main_hlayout.addWidget(self.textEdit)
        main_hlayout.addWidget(tab_widget)
        main_hlayout.setSizes([200, 500])
        main_hlayout.addWidget(self.console)

        layout.addWidget(menu_bar)
        layout.addWidget(main_hlayout, 2)
        layout.addLayout(btn_hlayout)

        self.setLayout(layout)

        # automatically updates register every x ms
        register_timer = QTimer(self)
        register_timer.setInterval(500)
        register_timer.timeout.connect(self.updateRegistersGUI)
        register_timer.start()

        # Load the file and display its contents
        self.loadFile()

        # Connect the cursor position changed signal to the onCursorPositionChanged method
        self.textEdit.mouseDoubleClickEvent = self.onMouseDoubleClickEvent

        # Load previously saved settings
        self.loadSettings()

        self.setup_runtime()

    def setup_runtime(self):
        self.R = Registers()
        self.I = Interpreter(self.filename, self.R)
        self.I.process()
        self.I.highlight_line.connect(self.updateLineGUI)
        self.register_box.setText("Registers:\n" + self.R.__str__())

    def loadFile(self):
        # Open the file and read its contents
        with open(self.filename, 'r') as file:
            text = file.read()

        # Add line numbers to the text
        lines = text.split('\n')
        padding = len(str(len(lines)))
        numberedText = '\n'.join([f'{i+1:0{padding}d}: {line}' for i, line in enumerate(lines)])

        # Set the text of the QTextEdit widget to the numbered text
        self.textEdit.setText(numberedText)
        self.textEditEdit.setText('\n'.join(lines))

    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Assembly Files (*.asm, *.s); All Files (*)")

        file_path, _ = file_dialog.getOpenFileName(self, "Open file", "", "Assembly Files (*.asm, *.s); All Files (*)")

        self.filename = file_path
        self.loadFile()
        self.R.clear_registers()
        self.setup_runtime()


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
            fmt.setBackground(QColor(25,25,25))

            cursor.setBlockFormat(fmt)
        except KeyError:
            breakpoints.GLOBAL_BREAKPOINTS[lineNumber] = lineText
            try:
                extracted_instruction = lineText.split(" ")[5] 
                if (((extracted_instruction in Instructions.get_all_instructions()) and (not Instructions.isLabel(breakpoints.consume_line_number_and_return_line(lineText)))) and (not Instructions.isDirective(breakpoints.consume_line_number_and_return_line(lineText)))): 
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
        self.I.state_of_step = False
        self.saveFile()
        self.setup_runtime()
        self.I.run()
        breakpoints.BUTTON_STACK.append("run")

    def stepCode(self):
        self.I.state_of_step = True
        breakpoints.STOP_AT_NEXT_INSTRUCTION = True
        self.I.step_button_pressed = True
        self.I.continue_button_pressed = False
        breakpoints.BUTTON_STACK.append("step")

    def continueCode(self):
        self.I.state_of_step = False
        breakpoints.STOP_AT_NEXT_INSTRUCTION = False
        self.I.step_button_pressed = False
        self.I.continue_button_pressed = True
        breakpoints.BUTTON_STACK.append("continue")

    def clearRegisters(self):
        self.R.clear_registers()
        self.register_box.setText("Registers:\n" + self.R.__str__())

    def saveFile(self):
        with open(self.filename, 'w') as fobj:
            fobj.write(self.textEditEdit.toPlainText())

        self.loadFile()

    def updateRegistersGUI(self):
        # Get the current scroll position
        scroll_bar = self.register_box.verticalScrollBar()
        scroll_pos = scroll_bar.value()

        self.register_box.setText("Registers:\n" + self.R.__str__())

        # Restore the scroll position
        scroll_bar.setValue(scroll_pos)

    @pyqtSlot(dict)
    def updateConsoleGUI(self, text):
        raise NotImplementedError("This method is not implemented yet")

    @pyqtSlot(dict)
    def updateLineGUI(self, currently_executing_object):
        self.instruction_box.setText(f"{currently_executing_object['instr']} at offset {currently_executing_object['index']} from {currently_executing_object['label']}")
        self.instruction_box.update()

        if currently_executing_object["instr"] == "EndOfInstruction":
            return None

        text = self.textEdit.toPlainText()
        lines = text.splitlines()

        last_label = None
        count_from_label = 0
        for x, i in enumerate(lines):
            line_number_from_instruction = breakpoints.return_line_number_from_GUI_instruction_line(i)
            fmt_line = breakpoints.consume_line_number_and_return_line(i).strip()
            if Instructions.isLabel(fmt_line):
                fmt_line = fmt_line[0:-1].strip() # remove colon and whitespace
                last_label = fmt_line
                count_from_label = 0
                continue

            if fmt_line == "":
                continue

            if fmt_line == "jal foo":
                pass

            if (currently_executing_object["label"] == last_label) and (currently_executing_object["index"] == count_from_label) and (currently_executing_object["instr"] == fmt_line):
                doc = self.textEdit.document()
                block = doc.findBlockByLineNumber(line_number_from_instruction - 1)
                char_fmt = QTextCharFormat()
                char_fmt.setForeground(Qt.yellow) 

                cursor = QTextCursor(block)
                cursor.select(QTextCursor.BlockUnderCursor)
                cursor.setCharFormat(char_fmt)

                # clear previous line
                if self.last_highlighted_line is not None:
                    block = doc.findBlockByLineNumber(self.last_highlighted_line - 1)
                    char_fmt = QTextCharFormat()
                    char_fmt.setForeground(Qt.white)

                    cursor = QTextCursor(block)
                    cursor.select(QTextCursor.BlockUnderCursor)
                    cursor.setCharFormat(char_fmt)

                self.textEdit.repaint()
                self.last_highlighted_line = line_number_from_instruction
                break

            count_from_label += 1

    def changeFont(self, from_settings=None):
        if from_settings is not None:
            font = QFont(from_settings)
            ok = True

        if from_settings is None:
            font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)
            self.textEditEdit.setFont(font)
            self.register_box.setFont(font)
            self.console.setFont(font)
            self.instruction_box.setFont(font)

            self.textEditEdit.setFontPointSize(self.textEdit.fontPointSize() if self.textEdit.fontPointSize() != 0.0 else 10)

            tab_width = self.textEditEdit.fontMetrics().width(' ') * 4
            self.textEdit.setTabStopWidth(tab_width)
            self.textEditEdit.setTabStopWidth(tab_width)

            self.settings.setValue("font", font.toString())

    def loadSettings(self):
        settings = self.settings

        if settings.contains("font"):
            self.changeFont(from_settings=settings.value("font"))

    def closeEvent(self, _event):
        self.saveFile()

