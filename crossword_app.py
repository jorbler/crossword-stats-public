from src.app_components import *

from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QFont
import sys
import json

class CWApp(qtw.QApplication):
    '''App that runs the program.'''
    def __init__(self) -> None:
        super().__init__([])

        self.load_user_info()
        self.main_window()
        sys.exit(self.exec_())
        return
    
    def load_user_info(self) -> None:
        '''Checks if user info exists. If not, a dialog window where user inputs info pops up. If it exists, the main window will open.'''
        try:
            with open('data/user_data.json') as f:
                self.user_data = json.load(f)
                self.user_cookie = self.user_data["user_cookie"]
                self.last_date = self.last_date["last_refresh_date"]
                print(self.user_cookie)
        except Exception as e:
            self.enter_cookie()

    def enter_cookie(self) -> None:
        '''Shows dialog window with input box for user to input their cookie.'''
        self.cookie = EnterCookie()
        self.cookie.show()
        return

    def main_window(self) -> None:
        '''Shows main window.'''
        self.main = MainWindow()
        self.main.show()
        return

if __name__ == "__main__":
    CWApp()