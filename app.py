from src.app_components import *

from PyQt5 import QtWidgets as qtw
from PyQt5.QtGui import QFont
import sys

class SimpleApp(qtw.QApplication):
    def __init__(self):
        super().__init__([])
        self.welcome_box()

    def welcome_box(self) -> None:
        intro_text = "Welcome to MyCrosswordBuddy! This app allows you to gain insight into your NYT Crossword data. \nTo access your data, you will need to enter the cookie associated with your NYT Games account.\n\nDo you need instructions on how to access your cookie?"
        welcome = YesNoPopUpWindow("Welcome!", intro_text)
        if welcome.exec() == qtw.QMessageBox.Yes:
            self.cookie_instructions()
        else: 
            print("no")

    def cookie_instructions(self) -> None:
        IntroMenuPages()

if __name__ == "__main__":
    SimpleApp()