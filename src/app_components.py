from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import os
import json

from src.create_graphs import *
from src.globals import *


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

        self.input_box = qtw.QLineEdit()
        self.input_box.setPlaceholderText("Enter your cookie here")
        self.input_box.setFixedSize(400, 40)

        self.ok_button = qtw.QPushButton("OK", self)

        self.ok_button.clicked.connect(self.save_cookie)
        #self.ok_button.clicked.connect(self.accept)

        

        self.my_layout = qtw.QVBoxLayout(self)
        self.my_layout.addWidget(self.welcome_text)
        self.my_layout.addWidget(self.input_box)
        self.my_layout.addWidget(self.ok_button)
        

    def save_cookie(self):
        self.cookie_value = self.input_box.text()
        user_dict = {"cookie":self.cookie_value}
        with open('data/user_data.json', 'w') as f:
            json.dump(user_dict, f)
        self.accept()
     

class CreateCanvas(FigureCanvasQTAgg):
    def __init__(self, fig):
        super().__init__(fig)


class DailyHistTab(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.day = "Monday"

        combo_box = qtw.QComboBox()
        combo_box.addItems(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        combo_box.currentTextChanged.connect(self.text_changed)

        layout = qtw.QVBoxLayout()
        layout.addWidget(combo_box)
        
        self.fig = qtw.QWidget()

        self.draw_hist()
        self.fig = plt.gcf()

        self.hist_widget = FigureCanvasQTAgg(self.fig)

        layout.addWidget(self.hist_widget)
        self.setLayout(layout)

    def draw_hist(self):
        create_hist(self.day)
        self.fig = plt.gcf()
        self.hist_widget = FigureCanvasQTAgg(self.fig)

    def text_changed(self, s):
        self.day = s
        print(self.day)
        self.draw_hist()

    
    
    
class DailyBarTab(qtw.QWidget):
    def __init__(self):
        super().__init__()

        layout = qtw.QVBoxLayout()
        self.setLayout(layout)

        create_compare_ave_times()
        self.fig = plt.gcf()

        layout.addWidget(FigureCanvasQTAgg(self.fig))
        self.setLayout(layout)


class DailyTab(qtw.QWidget):
    def __init__(self):
        super().__init__()

        layout = qtw.QVBoxLayout()
        tab_widget = qtw.QTabWidget()


        self.hist_tab = DailyHistTab()
        self.bar_tab = DailyBarTab()
        
        tab_widget.addTab(self.hist_tab, "Daily Histograms")
        tab_widget.addTab(self.bar_tab, "Ave. Times Bar Chart")

        layout.addWidget(tab_widget)
        self.setLayout(layout)

        


class MiniTab(qtw.QWidget):
    def __init__(self):
        super().__init__()


class BonusTab(qtw.QWidget):
    def __init__(self):
        super().__init__()


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        layout = qtw.QHBoxLayout()
        self.setLayout(layout)


        self.left_panel = qtw.QListWidget()

        self.left_panel.addItem("Daily")
        self.left_panel.addItem("Mini")
        self.left_panel.addItem("Bonus")

        self.left_panel.currentRowChanged.connect(self.change_page)
        
        self.left_panel_pages = qtw.QStackedWidget()
        daily = DailyTab()
        mini = MiniTab()
        bonus = BonusTab()
        
        self.left_panel_pages.addWidget(daily)
        self.left_panel_pages.addWidget(mini)
        self.left_panel_pages.addWidget(bonus)
        
        

        layout.addWidget(self.left_panel, 1)
        layout.addWidget(self.left_panel_pages, 4)
        
        self.left_panel.setCurrentRow(0)

    def change_page(self, index):
        self.left_panel_pages.setCurrentIndex(index)