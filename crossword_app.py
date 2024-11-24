from src.app_components import *

from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QFont
import sys

class CWApp(qtw.QApplication):
    def __init__(self):
        super().__init__([])

        self.enter_cookie()

        sys.exit(self.exec_())
        return

    def enter_cookie(self):
        self.cookie = EnterCookie()
        self.cookie.show()
        self.user_cookie = self.cookie.get_cookie() 
        return

    def main_window(self):
        return



if __name__ == "__main__":
    CWApp()