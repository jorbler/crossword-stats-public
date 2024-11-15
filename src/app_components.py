from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import Qt
import sys

class WelcomeDialog(qtw.QMessageBox):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Welcome!")

        self.needs_instructions = False

        layout = qtw.QVBoxLayout()

        intro_text = """
                    Welcome to MyCrosswordBuddy! This app allows you to gain insight into your NYT Crossword data. 
                    To access your data, you will need to enter the cookie associated with your NYT Games account.
                    Do you need instructions on how to access your cookie?
                    """
        welcome_label = qtw.QLabel(intro_text, self)
        layout.addWidget(welcome_label)

        # yes_button = qtw.QPushButton("Yes")
        # no_button = qtw.QPushButton("No")

        # yes_button.clicked.connect(self.set_instructions_needed)
        # no_button.clicked.connect(self.close_dialog)

        # layout.addWidget(yes_button)
        # layout.addWidget(no_button)

        self.setLayout(layout)