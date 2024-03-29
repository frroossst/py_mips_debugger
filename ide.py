# GUI imports
from PyQt5.QtGui import QTextBlockFormat, QIcon, QColor, QTextCursor, QTextCharFormat, QFontMetrics, QFont
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, QMenuBar, QAction, QFileDialog, QSplitter, QTabWidget, QSizePolicy, QFontDialog, QToolTip, QMessageBox, QListWidget, QDialog, QComboBox, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, QSettings, QFileSystemWatcher, QEvent, QCoreApplication

# Runtime imports
from exceptions import InterpreterConversionError
from better_data_structures import better_deque
from syntax_highlighter import MIPSHighlighter
from instructions import Instructions
from interpreter import Interpreter
from registers import Registers
from syscalls import Syscall
from memory import Memory
from asm_doc import AsmDoc
import breakpoints
import queue


class IDE(QWidget):

    filename = None
    settings = QSettings("PyMIPS", "PyMIPS Emulator")
    last_added_breakpoint = None

    R = None # Registers
    M = None # Memory
    I = None # Interpreter

    register_box = None 

    last_highlighted_line = None

    def __init__(self, filename):
        self.filename = filename
        super().__init__()
        self.initUI()
        self.setMinimumSize(1080, 720)

    def initUI(self):
        self.setWindowTitle("PyMIPS Emulator (" + self.filename + ")")
        self.setWindowIcon(QIcon('./assets/icon.png'))

        tab_width = 4 * QFontMetrics(self.font()).width(' ')

        # Create the QTextEdit widget to display the file contents
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.setTabStopWidth(tab_width)
        self.textEdit.setLineWrapMode(QTextEdit.NoWrap)

        # Create the QTextEdit widget to edit the file contents
        self.textEditEdit = QTextEdit(self)
        self.textEditEdit.setReadOnly(False)
        self.textEditEdit.setFontPointSize(self.textEdit.fontPointSize() if self.textEdit.fontPointSize() != 0.0 else 10)
        self.textEditEdit.setTabStopWidth(tab_width)
        self.textEditEdit.setLineWrapMode(QTextEdit.NoWrap)

        # Create a syntax highlighter for the textEditEdit widget
        self.highlighter = MIPSHighlighter(self.textEditEdit.document())
        self.highlighter.setDocument(self.textEditEdit.document())

        # Registers Window
        self.register_box = QTextEdit(self)
        self.register_box.setReadOnly(True)
        self.register_box.setText("Registers:\n" + self.R.__str__())

        # Memory Window
        self.memory_box = QTextEdit(self)
        self.memory_box.setReadOnly(True)
        self.memory_box.setText("Memory:\n" + self.M.__str__())

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
        vim_action = QAction("Vim Mode", self)
        vim_action.triggered.connect(self.toggleVimMode)
        edit_menu.addAction(vim_action)

        debug_menu = menu_bar.addMenu("Debug")
        watch_action = QAction("Watch", self)
        watch_action.triggered.connect(self.watchPanel)
        debug_menu.addAction(watch_action)

        window_menu = menu_bar.addMenu("Window")
        watchpanel_action = QAction("Watch Panel", self)
        watchpanel_action.triggered.connect(self.watchDebugPanel)
        watchpanel_action.setCheckable(True)
        window_menu.addAction(watchpanel_action)

        # Instructin viewer window
        self.instruction_box = QTextEdit(self)
        self.instruction_box.setReadOnly(True)
        self.instruction_box.setText("Hit RUN to start the emulator")
        self.instruction_box.setMaximumHeight(45)
        self.instruction_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create CLEAR button
        clear_button = QPushButton("CLEAR", self)
        clear_button.setToolTip("Reset the emulator and clear registers and consoles")
        clear_button.clicked.connect(self.clearButton)
        btn_hlayout.addWidget(clear_button)

        # Create RUN button
        run_button = QPushButton("RUN", self)
        run_button.setToolTip("Run the program")
        run_button.clicked.connect(self.runCode)
        btn_hlayout.addWidget(run_button)

        # Create STEP button
        step_button = QPushButton("STEP", self)
        step_button.setToolTip("Step through the program one instruction at a time")
        step_button.clicked.connect(self.stepCode)
        btn_hlayout.addWidget(step_button)

        # Create CONTINUE button
        continue_button = QPushButton("CONTINUE", self)
        continue_button.setToolTip("Continue running the program until the next breakpoint")
        continue_button.clicked.connect(self.continueCode)
        btn_hlayout.addWidget(continue_button)

        # Tabs     view, edit
        tab_widget = QTabWidget()
        tab_widget.addTab(self.textEdit, "View")
        tab_widget.addTab(self.textEditEdit, "Edit")
        
        # to save the file when switching tabs
        tab_widget.currentChanged.connect(self.saveFile)

        # Tabs     registers, memory
        tab_widget2 = QTabWidget()
        tab_widget2.addTab(self.register_box, "Registers")
        tab_widget2.addTab(self.memory_box, "Memory")

        # registers, mems, instructions
        regmem_ins_lay = QSplitter(Qt.Vertical)
        regmem_ins_lay.addWidget(tab_widget2)
        regmem_ins_lay.addWidget(self.instruction_box)
        regmem_ins_lay.setSizes([200, 10])

        # Constructing the console window
        self.consoleEdit = QTextEdit(self)
        self.consoleEdit.setReadOnly(True)
        self.consoleEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.consoleEdit.setAcceptRichText(False)
        self.consoleEdit.setText("Console:\n")
        self.consoleEdit.textChanged.connect(self.onConsoleTextChange)
        self.consoleEdit.keyPressEvent = self.onConsoleKeyPressEvent
        self.takeConsoleInput = False

        main_hlayout.addWidget(regmem_ins_lay)
        main_hlayout.setSizes([200, 500])
        main_hlayout.addWidget(tab_widget)
        main_hlayout.setSizes([200, 500])
        main_hlayout.addWidget(self.consoleEdit)

        layout.addWidget(menu_bar)
        layout.addWidget(main_hlayout, 2)
        layout.addLayout(btn_hlayout)

        self.setLayout(layout)

        # automatically updates register every x ms
        register_timer = QTimer(self)
        register_timer.setInterval(500)
        register_timer.timeout.connect(self.updateRegistersGUI)
        register_timer.start()

        # automatically updates watch expressions every x ms
        self.watch_debug_window = None
        watch_timer = QTimer(self)
        watch_timer.setInterval(500)
        watch_timer.timeout.connect(self.updateWatchGUI)
        watch_timer.start()

        # automatically updates memory every x ms
        memory_timer = QTimer(self)
        memory_timer.setInterval(500)
        memory_timer.timeout.connect(self.updateMemoryGUI)
        memory_timer.start()

        # automatically re-highlight breakpoints and current line every x ms
        highlight_timer = QTimer(self)
        highlight_timer.setInterval(250)
        highlight_timer.timeout.connect(self.reHighlightLines)
        highlight_timer.start()

        # every x ms, remind the user that the program is waiting on an input
        self.wfi_print_timer = QTimer()
        self.wfi_print_timer.setInterval(1000)
        # ! starts when console receives stdin object
        self.wfi_print_timer.timeout.connect(self.print_wfi_message)

        # watch the current file for changes and reload
        self.file_watcher = QFileSystemWatcher([self.filename])
        self.file_watcher.fileChanged.connect(self.loadFile)

        # Load the file and display its contents
        self.loadFile()

        # Connect the cursor position changed signal to the onCursorPositionChanged method
        self.textEdit.mouseDoubleClickEvent = self.onMouseDoubleClickEvent
        self.textEdit.mousePressEvent = self.onMouseSingleClickEvent

        # Load previously saved settings
        self.loadSettings()

        # Setup the runtime environment for the Interpreter
        self.setup_runtime()

    def setup_runtime(self):
        self.R = Registers()
        self.M = Memory()
        self.S = Syscall()
        self.I = Interpreter(self.filename, self.R, self.M, self.S)
        self.I.process()
        self.I.highlight_line.connect(self.updateLineGUI)
        self.S.console_signal.connect(self.updateConsoleGUI)
        self.I.rehighlight_signal.connect(self.reHighlightLines)
        self.register_box.setText("Registers:\n" + self.R.__str__())
        self.consoleEdit.blockSignals(True)
        self.consoleEdit.setText("Console:\n")
        self.consoleEdit.blockSignals(False)

    def loadFile(self):
        # Open the file and read its contents
        with open(self.filename, 'r') as file:
            text = file.read()

        # Add line numbers to the text
        lines = text.split('\n')
        padding = len(str(len(lines)))
        numberedText = '\n'.join([f'{i+1:0{padding}d}: {line}' for i, line in enumerate(lines)])

        # make \t 4 spaces to ensure consistency in spacing
        numberedText = numberedText.replace('\t', '    ')

        # Set the text of the QTextEdit widget to the numbered text
        self.textEdit.setText(numberedText)
        self.textEditEdit.setText('\n'.join(lines))
        self.textEditEdit.update()

    def open_file_dialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Assembly Files (*.asm, *.s); All Files (*)")

        file_path, _ = file_dialog.getOpenFileName(self, "Open file", "", "Assembly Files (*.asm, *.s); All Files (*)")

        if file_path != self.filename:
            breakpoints.GLOBAL_BREAKPOINTS = {}
            breakpoints.INTERPRETED_BREAKPOINTS = {}
            breakpoints.STOP_AT_NEXT_INSTRUCTION = False
            breakpoints.MESSAGE_QUEUE = queue.Queue()
            breakpoints.BUTTON_STACK = better_deque()
            breakpoints.CURRENT_EXECUTING_OBJECT = {}

        self.filename = file_path
        self.loadFile()
        self.R.clear_registers()
        self.setup_runtime()

    def onMouseSingleClickEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            cursor = self.textEdit.cursorForPosition(event.pos())

            # get word under cursor
            cursor.select(QTextCursor.WordUnderCursor)
            word_under_cursor = cursor.selectedText().strip().strip(":")
            fmt_tip = AsmDoc.get_asm_doc(word_under_cursor)

            QToolTip.showText(event.globalPos(), fmt_tip, self.textEdit)

    def onMouseDoubleClickEvent(self, event):
        # Get the current line number
        cursor = self.textEdit.cursorForPosition(event.pos())
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

    def clearButton(self):
        self.consoleEdit.blockSignals(True)
        self.R.clear_registers()
        self.register_box.setText("Registers:\n" + self.R.__str__())
        self.memory_box.setText("Memory:\n" + self.M.__str__())
        self.consoleEdit.setText("Console:\n")
        self.consoleEdit.blockSignals(False)
        self.setup_runtime()
        self.reference_console_text = self.consoleEdit.toPlainText()

    def saveFile(self):
        with open(self.filename, 'w') as fobj:
            fobj.write(self.textEditEdit.toPlainText())

        self.loadFile()

    def watchFile(self):
        if self.file_watcher.files():
            print("File is being watched")
        else:
            print("File is not being watched")

    def updateRegistersGUI(self):
        # Get the current scroll position
        scroll_bar = self.register_box.verticalScrollBar()
        scroll_pos = scroll_bar.value()

        self.register_box.setText("Registers:\n" + self.R.__str__())

        # look through each line and highgliht if dounf
        cursor = self.register_box.textCursor()

        prev_hotmap = self.R.register_hotmap
        curr_hotmap = []
        if len(prev_hotmap) < 3:
            curr_hotmap.extend(["invalid", "invalid", "invalid"])
        else:
            curr_hotmap = self.R.register_hotmap

        for i in range(self.register_box.document().blockCount()):
            cursor.setPosition(self.register_box.document().findBlockByLineNumber(i).position())

            if cursor.block().text().startswith(curr_hotmap[2]):
                char_fmt = QTextCharFormat()
                char_fmt.setForeground(Qt.red)
                cursor.setCharFormat(char_fmt)
                cursor.select(QTextCursor.LineUnderCursor)
                cursor.setCharFormat(char_fmt)

            elif cursor.block().text().startswith(curr_hotmap[1]):
                char_fmt = QTextCharFormat()
                char_fmt.setForeground(QColor(255, 128, 0)) # orange
                cursor.setCharFormat(char_fmt)
                cursor.select(QTextCursor.LineUnderCursor)
                cursor.setCharFormat(char_fmt)

            elif cursor.block().text().startswith(curr_hotmap[0]):
                char_fmt = QTextCharFormat()
                char_fmt.setForeground(Qt.yellow)
                cursor.setCharFormat(char_fmt)
                cursor.select(QTextCursor.LineUnderCursor)
                cursor.setCharFormat(char_fmt)

        # Restore the scroll position
        scroll_bar.setValue(scroll_pos)

    def produce_memory_table(self):
        data = self.M.__str__().splitlines()
        table_start = "<table>"
        header = "<tr><th>Address</th><th>Value</th></tr>"
        table_end = "</table>"
        table_data = [ f"<tr><td>{x.split(':')[0]}</td> <td>{x.split(':')[1]}</td></tr>" for x in data if x != ""]
        return table_start + header + "".join(table_data) + table_end 

    def updateMemoryGUI(self):
        # Get the current scroll position
        scroll_bar = self.memory_box.verticalScrollBar()
        scroll_pos = scroll_bar.value()

        self.memory_box.setHtml(self.produce_memory_table())

        # Restore the scroll position
        scroll_bar.setValue(scroll_pos)

    def eventFilter(self, _obj, event):
        if event.type() == QEvent.KeyPress and event.key() == 16777220:
            self.consoleEdit.setReadOnly(True)

    def onConsoleTextChange(self):
        curr_text = self.consoleEdit.toPlainText()
        try:
            if self.reference_console_text not in curr_text:
                QMessageBox.warning(self, "Error", "You cannot edit the stdout console")
                self.consoleEdit.setText(self.reference_console_text)
                self.consoleEdit.moveCursor(QTextCursor.End)
        except AttributeError:
            pass

    def print_wfi_message(self):
        print("waiting for input")

    def onConsoleKeyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.consoleEdit.setReadOnly(True)
            self.takeConsoleInput = False
            self.wfi_print_timer.stop()

        if event.key() == Qt.Key_Backspace:
            cursor = self.consoleEdit.textCursor()
            cursor.deletePreviousChar()
            return None

        super().keyPressEvent(event)
        self.consoleEdit.setText(self.consoleEdit.toPlainText() + event.text())
        self.consoleEdit.moveCursor(QTextCursor.End)

    @pyqtSlot(dict)
    def updateConsoleGUI(self, console_object):
        prev_console_content = self.consoleEdit.toPlainText()
        if console_object["operation"] == "stdout":
            self.consoleEdit.append(console_object["data"])

        elif console_object["operation"] == "stdin":
            self.consoleEdit.setReadOnly(False)
            self.consoleEdit.setFocus()
            self.consoleEdit.moveCursor(QTextCursor.End)
            self.reference_console_text = self.consoleEdit.toPlainText()

            self.wfi_print_timer.start()

            self.takeConsoleInput = True
            while (self.takeConsoleInput):
                QCoreApplication.processEvents()
                self.reHighlightLines()

            self.consoleEdit.setReadOnly(True)
            self.consoleEdit.clearFocus()
            self.reHighlightLines()

            if console_object["type"] == "int":
                try:
                    input_received = int(self.consoleEdit.toPlainText().removeprefix(prev_console_content).strip("\n"))
                    self.R.set_register("v0", input_received)
                except Exception:
                    raise InterpreterConversionError("Input was not an integer")

            elif console_object["type"] == "str":
                input_received = self.consoleEdit.toPlainText().removeprefix(prev_console_content).strip("\n")[:console_object["data"]["str_len"]:]
                self.M.store_existing_string(input_received, console_object["data"]["str_addr"])

            elif console_object["type"] == "char":
                input_received = self.consoleEdit.toPlainText().removeprefix(prev_console_content).strip("\n")[0]
                self.R.set_register("v0", ord(input_received))

        self.reHighlightLines()

    @pyqtSlot()
    def reHighlightLines(self):
        doc = self.textEdit.document()

        for i in breakpoints.GLOBAL_BREAKPOINTS:
            block = doc.findBlockByLineNumber(i - 1)
            fmt = QTextBlockFormat()
            fmt.setBackground(Qt.red)

            cursor = QTextCursor(block)
            cursor.setBlockFormat(fmt)

        if {} != breakpoints.CURRENT_EXECUTING_OBJECT:
            line_num = breakpoints.get_line_number_from_label_index(self.textEdit.toPlainText(), breakpoints.CURRENT_EXECUTING_OBJECT["label"], breakpoints.CURRENT_EXECUTING_OBJECT["index"])
            if line_num is None:
                return None
            
            block = doc.findBlockByLineNumber(line_num)

            fmt = QTextBlockFormat()
            fmt.setForeground(Qt.yellow)

            cursor = QTextCursor(block)
            cursor.setBlockFormat(fmt)

            self.textEdit.repaint()

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

            if fmt_line.startswith("#"):
                continue

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

                self.textEdit.update()
                self.last_highlighted_line = line_number_from_instruction
                
                # set red bg for breakpoints
                for breakpoint_line in breakpoints.GLOBAL_BREAKPOINTS:
                    block = doc.findBlockByLineNumber(breakpoint_line - 1)
                    fmt = QTextBlockFormat()
                    fmt.setBackground(Qt.red)

                    cursor = QTextCursor(block)
                    cursor.setBlockFormat(fmt)

                break

            count_from_label += 1

    def changeFont(self, from_settings=None):
        if from_settings is not None and from_settings is not False:
            font = QFont(from_settings)
            ok = True

        if from_settings is None or from_settings is False:
            font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)
            self.textEditEdit.setFont(font)
            self.register_box.setFont(font)
            self.memory_box.setFont(font)
            self.consoleEdit.setFont(font)
            self.instruction_box.setFont(font)

            self.textEditEdit.setFontPointSize(self.textEdit.fontPointSize() if self.textEdit.fontPointSize() != 0.0 else 10)

            tab_width = self.textEditEdit.fontMetrics().width(' ') * 4
            self.textEdit.setTabStopWidth(tab_width)
            self.textEditEdit.setTabStopWidth(tab_width)

            self.settings.setValue("font", font.toString())

    def toggleVimMode(self):
        raise RuntimeError("Not implemented")

    def watchPanel(self):
        box = QDialog(self)
        box.setWindowTitle("Watch Panel")

        layout = QGridLayout(box)

        watch_list = QListWidget(box)
        for i in breakpoints.WATCHED_EXPRESSIONS:
            watch_list.addItem(i["register_source"] + i["operator"] + i["register_target"])

        register_dropdown = QComboBox(box)
        for i in self.R.get_all_registers_as_list():
            register_dropdown.addItem(i)

        operator_dropdown = QComboBox(box)
        operator_dropdown.addItem("==")
        operator_dropdown.addItem("!=")
        operator_dropdown.addItem("<")
        operator_dropdown.addItem(">")
        operator_dropdown.addItem("<=")
        operator_dropdown.addItem(">=")

        value_input = QLineEdit(box)

        add_btn = QPushButton("Add", box)
        add_btn.clicked.connect(lambda: self.verify_and_add_watch_expression(watch_list, f"{register_dropdown.currentText()} {operator_dropdown.currentText()} {value_input.text()}"))

        remove_btn = QPushButton("Remove", box)
        remove_btn.clicked.connect(lambda: breakpoints.remove_watch_expression(f"{register_dropdown.currentText()} {operator_dropdown.currentText()} {value_input.text()}"))
        remove_btn.clicked.connect(lambda: watch_list.takeItem(watch_list.currentRow()))

        layout.addWidget(watch_list, 0, 0, 1, 3)
        layout.addWidget(register_dropdown, 1, 0)
        layout.addWidget(operator_dropdown, 1, 1)
        layout.addWidget(value_input, 1, 2)
        layout.addWidget(add_btn, 2, 0, 1, 3)
        layout.addWidget(remove_btn, 3, 0, 1, 3)

        box.exec()
        
    def watchDebugPanel(self, action):
        if action:
            # create a new window
            self.watch_debug_window = QDialog(self)
            self.watch_debug_window.setWindowTitle("Watch Debug Panel")

            layout = QGridLayout(self.watch_debug_window)

            self.watch_debug_list = QListWidget(self.watch_debug_window)
            for i in breakpoints.EVALUATED_WATCHED_EXPRESSIONS:
                self.watch_debug_list.addItem(i["register_source"] + i["operator"] + i["register_target"])

            layout.addWidget(self.watch_debug_list, 0, 0, 1, 3)

            self.watch_debug_window.show()
        else:
            self.watch_debug_window = None
            self.watch_debug_window.close()

    def updateWatchGUI(self):
        if self.watch_debug_window is not None:
            self.watch_debug_list = QListWidget(self.watch_debug_window)
            for i in breakpoints.EVALUATED_WATCHED_EXPRESSIONS:
                self.watch_debug_list.addItem(i["register_source"] + i["operator"] + i["register_target"])

    def verify_and_add_watch_expression(self, wlref, expression):
        li = expression.split(" ")
        src, op, target = li[0], li[1], li[2]

        # verify that target is a register or a number
        if not (target.isnumeric() or self.R.get_register_validity(target)):
            QMessageBox.warning(self, "Invalid expression", "Target must be a register or a number")
            return None

        breakpoints.add_watch_expression(src, op, target)
        wlref.addItem(expression)

    def loadSettings(self):
        settings = self.settings

        if settings.contains("font"):
            self.changeFont(from_settings=settings.value("font"))

        # TODO: allow custom syntax highlighting

    def closeEvent(self, _event):
        self.saveFile()
