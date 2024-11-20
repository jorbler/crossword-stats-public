from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import sys
import os

class YesNoPopUpWindow(qtw.QMessageBox):
    '''
    Creates a dialog box with body text
    '''
    def __init__(self, title, body_text):
        super().__init__()
        
        self.setWindowTitle(title)
        self.setText(body_text)
        self.setStandardButtons(qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        self.setDefaultButton(qtw.QMessageBox.Yes)
        self.setFont(QFont("Arial", 14, weight = 1))

class WelcomeWindow(YesNoPopUpWindow):
    '''
    Welcome window that appears to the user the first time that they open the app.
    '''
    def __init__(self):
        intro_text = "Welcome to MyCrosswordBuddy! This app allows you to gain insight into your NYT Crossword data. \nTo access your data, you will need to enter the cookie associated with your NYT Games account.\n\nDo you need instructions on how to access your cookie?"
        super().__init__("Welcome!", intro_text)

class MenuPage(qtw.QVBoxLayout):
    def __init__(self, text, rel_image_path = None):
        super().__init__()
        self.create_page(text, rel_image_path)

    def create_page(self, text, rel_image_path = None):
        page_text = qtw.QLabel()
        page_text.setText(text)
        self.addWidget(page_text)
        if rel_image_path:
            page_image = qtw.QLabel()
            page_image.setPixmap(QPixmap(os.getcwd() + rel_image_path))
            self.addWidget(page_image)


class IntroMenuPages(qtw.QComboBox):
    '''
    Menu that has next and previous arrows that switch the "page" of the menu.
    '''
    def __init__(self):
        super().__init__()
        self.create_pages()
    
    def create_pages(self):
        stacked_widget =  qtw.QStackedWidget()

        page1 = MenuPage("Open https://www.nytimes.com/crosswords in Google Chrome.\n\nLog in to your account if not already logged in.")
        page2 = MenuPage("Click on the three dots in the top right corner of the window.", "src/images/menu1.png")
        page3 = MenuPage("Click on \"More Tools\" and then \"Developer Tools\"", "src/images/menu2.png")
        page4 = MenuPage("Click on \"Application\"", "src/images/menu3.png")
        page5 = MenuPage(" On the left panel, click \"Cookies\"; this will show a drop-down menu below. Click on \"https://nytimes.com\"", "src/images/menu4.png")
        page6 = MenuPage(""" Under the \"Name\" column, scroll down to find \"NYT-S\". 
                         The value for your cookie will be in the \"Value\" column, however it will be truncated. 
                         Click on \"NYT-S\" in the \"Name\" column. Your full cookie will be in the bottom panel (showed below). 
                         Highlight the full cookie and copy it.""", "src/images/menu5.png")
        
        stacked_widget.addWidget(page1)
        stacked_widget.addWidget(page2)
        stacked_widget.addWidget(page3)
        stacked_widget.addWidget(page4)
        stacked_widget.addWidget(page5)
        stacked_widget.addWidget(page6)


        self.addItem("Step 1")
        self.addItem("Step 2")
        self.addItem("Step 3")
        self.addItem("Step 4")
        self.addItem("Step 5")
        self.addItem("Step 6")
        
        self.activated[int].connect(stacked_widget.setCurrentIndex)


        


