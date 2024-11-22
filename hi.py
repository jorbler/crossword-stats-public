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
        self.welcome = IntroMenuPages()
        self.welcome.show()


if __name__ == "__main__":
    SimpleApp()
