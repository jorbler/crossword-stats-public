from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
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

class MenuPage(qtw.QWidget):
    def __init__(self, text, rel_image_path = None):
        super().__init__()
        layout = qtw.QVBoxLayout()
        layout.addWidget(qtw.QLabel(text))

        if rel_image_path:
            page_image = qtw.QLabel()
            page_image.setPixmap(QPixmap(os.getcwd() + rel_image_path))
            layout.addWidget(page_image)
        self.setLayout(layout)

class IntroMenuPages(qtw.QWidget):
    '''
    Menu that has next and previous arrows that switch the "page" of the menu.
    '''
    def __init__(self):
        super().__init__()
        self.create_pages()
        self.setWindowTitle("Cookie Instructions")
        self.resize(400, 300)
        self.show()
    
    def create_pages(self):
        layout = qtw.QVBoxLayout()

        page1 = MenuPage("Open https://www.nytimes.com/crosswords in Google Chrome.\n\nLog in to your account if not already logged in.")
        page2 = MenuPage("Click on the three dots in the top right corner of the window.", "src/images/menu1.png")
        page3 = MenuPage("Click on \"More Tools\" and then \"Developer Tools\"", "src/images/menu2.png")
        page4 = MenuPage("Click on \"Application\"", "src/images/menu3.png")
        page5 = MenuPage(" On the left panel, click \"Cookies\"; this will show a drop-down menu below. Click on \"https://nytimes.com\"", "src/images/menu4.png")
        page6 = MenuPage(""" Under the \"Name\" column, scroll down to find \"NYT-S\". 
                            The value for your cookie will be in the \"Value\" column, however it will be truncated. 
                            Click on \"NYT-S\" in the \"Name\" column. Your full cookie will be in the bottom panel (showed below). 
                            Highlight the full cookie and copy it.""", "src/images/menu5.png")
        
        self.stacked_widget = qtw.QStackedWidget()
        layout.addWidget(self.stacked_widget)

        self.stacked_widget.addWidget(page1)
        self.stacked_widget.addWidget(page2)
        self.stacked_widget.addWidget(page3)
        self.stacked_widget.addWidget(page4)
        self.stacked_widget.addWidget(page5)
        self.stacked_widget.addWidget(page6)

        self.setLayout(layout)

        next_prev_buttons = qtw.QVBoxLayout()

        self.prev_button = qtw.QPushButton("Back")
        self.next_button = qtw.QPushButton("Next")

        next_prev_buttons.addWidget(self.prev_button)
        next_prev_buttons.addWidget(self.next_button)
        
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)

        layout.addLayout(next_prev_buttons)

        self.update_buttons()

    def next_page(self):
        '''Go to next page in a stacked widget'''
        cur_index = self.stacked_widget.currentIndex()
        if cur_index < self.stacked_widget.count() -1:
            self.stacked_widget.setCurrentIndex(cur_index + 1)
        self.update_buttons()
    
    def prev_page(self):
        '''Go to previous page in a stacked widget'''
        cur_index = self.stacked_widget.currentIndex()
        if cur_index > 0:
            self.stacked_widget.setCurrentIndex(cur_index - 1)
        self.update_buttons()

    def update_buttons(self):
        '''Change button states based on the current index'''
        cur_index = self.stacked_widget.currentIndex()
        total_pages = self.stacked_widget.count()

        self.prev_button.setEnabled(cur_index > 0)
        self.next_button.setEnabled(cur_index < (total_pages - 1))

class EnterCookie(qtw.QDialog):
    '''A popup window that prompts the user to enter their cookie into a text box.'''

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Welcome!')

        self.welcome_text = qtw.QLabel("Welcome to MyCrosswordBuddy! This app allows you to gain insight into your NYT Crossword data. \nTo access your data, you will need to enter the cookie associated with your NYT Games account.\n\nDo you need instructions on how to access your cookie?")        

        self.input_box = qtw.QLineEdit(self)
        self.input_box.setPlaceholderText("Enter your cookie here")
        self.input_box.setFixedSize(400, 40)

        self.ok_button = qtw.QPushButton("OK", self)

        self.ok_button.clicked.connect(self.accept)
        print(self.input_box.text())
        self.cookie_value = self.input_box.text()

        self.my_layout = qtw.QVBoxLayout(self)
        self.my_layout.addWidget(self.welcome_text)
        self.my_layout.addWidget(self.input_box)
        self.my_layout.addWidget(self.ok_button)
        return

    def get_cookie(self):
        return self.cookie_value