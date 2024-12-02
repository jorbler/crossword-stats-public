from src.app_components import *

from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QFont
import sys
import json

class CWApp(qtw.QApplication):
    def __init__(self):
        super().__init__([])
        self.has_info = None

        self.load_user_info()
        if self.has_info:
            self.main_window()
        sys.exit(self.exec_())
        return
    
    def load_user_info(self):
        try:
            with open('data/user_data.json') as f:
                self.user_cookie = json.load(f)["cookie"]
                print(self.user_cookie)
                self.has_info = True
        except Exception as e:
            self.has_info = False
            self.enter_cookie()
        return

    def enter_cookie(self):
        self.cookie = EnterCookie()
        self.cookie.show()
        return

    def main_window(self):
        self.main = MainWindow()
        self.main.show()
        return

if __name__ == "__main__":
    CWApp()