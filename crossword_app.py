from src.app_components import *

from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QFont
import sys

class CWApp(qtw.QApplication):
    def __init__(self):
        super().__init__([])
        self.instructions = None
        self.enter_cookie()
        sys.exit(self.exec_())

    def enter_cookie(self):
        self.cookie = EnterCookie()
        self.cookie.show()
        self.user_cookie = self.cookie.get_cookie()
        print(self.user_cookie)




if __name__ == "__main__":
    CWApp()