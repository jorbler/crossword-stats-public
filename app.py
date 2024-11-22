from src.app_components import *

from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QFont
import sys

class SimpleApp(qtw.QApplication):
    def __init__(self):
        super().__init__([])
        self.instructions = None
        self.welcome_box()
        sys.exit(self.exec_())

    def welcome_box(self) -> None:
        welcome = WelcomeWindow()
        if welcome.exec() == qtw.QMessageBox.Yes:
            self.cookie_instructions()
        self.enter_cookie()

    def cookie_instructions(self) -> None:
        self.instructions = IntroMenuPages()
        self.instructions.show()

    def enter_cookie(self):
        self.cookie = EnterCookie()
        self.cookie.show()
        

if __name__ == "__main__":
    SimpleApp()
