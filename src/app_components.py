from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5 import QtCore as qtc
from PyQt5.QtGui import QFont, QPixmap
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from datetime import date
import os
import pandas as pd
import json

from src.get_all_data import *
from src.create_graphs import *
from src.globals import *
import src.data_refresh

class YesNoPopUpWindow(qtw.QMessageBox):
    '''
    Creates a dialog box with title, body text, and Yes/No buttons.
    '''
    def __init__(self, title: str, body_text: str):
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
        
        self.my_layout = qtw.QVBoxLayout(self)
        self.my_layout.addWidget(self.welcome_text)
        self.my_layout.addWidget(self.input_box)
        self.my_layout.addWidget(self.ok_button)
        
    def save_cookie(self):
        self.cookie_value = self.input_box.text()
        user_dict = {"cookie":self.cookie_value}
        with open('data/user_data.json', 'w') as f:
            json.dump(user_dict, f)
        self.init_load = InitalLoadData()
        self.init_load.show()
        self.accept()


class DailyHistTab(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.day = "Monday"

        combo_box = qtw.QComboBox()
        combo_box.addItems(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        combo_box.currentTextChanged.connect(self.text_changed)

        layout = qtw.QVBoxLayout()
        layout.addWidget(combo_box)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.hist_widget = FigureCanvasQTAgg(self.fig)
        layout.addWidget(self.hist_widget)
        
        self.setLayout(layout)
        self.draw_hist()

    def draw_hist(self):
        self.ax.clear()
        create_hist(self.day, self.ax)
        self.hist_widget.draw() 

    def text_changed(self, s):
        self.day = s
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


class DailyGraphsTab(qtw.QWidget):
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


class DailyTableTab(qtw.QWidget):
    def __init__(self):
        super().__init__()

        daily_df = daily_table()
        table_widget = TableWidget(daily_df, ["Time","Date","Day"])

        layout = qtw.QVBoxLayout()

        layout.addWidget(table_widget)
        self.setLayout(layout)


class DailyTab(qtw.QWidget):
    def __init__(self):
        super().__init__()

        layout = qtw.QVBoxLayout()
        tab_widget = qtw.QTabWidget()

        self.graphs_tab = DailyGraphsTab()
        self.tables_tab = DailyTableTab()

        tab_widget.addTab(self.graphs_tab, "Graphs")
        tab_widget.addTab(self.tables_tab, "Table View")

        layout.addWidget(tab_widget)
        self.setLayout(layout)

        
class MiniGraphTab(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.days = 30
        self.ax_box = None

        self.buttons_dict = {"Last 30 Days": 30,
                             "Last 60 Days": 60,
                             "Last 100 Days": 100
                             }

        self.day_button_30 = qtw.QRadioButton("Last 30 Days")
        self.day_button_60 = qtw.QRadioButton("Last 60 Days")
        self.day_button_100 = qtw.QRadioButton("Last 100 Days")

        self.day_button_30.setChecked(True)

        self.day_buttons = qtw.QButtonGroup(self)
        self.day_buttons.addButton(self.day_button_30)
        self.day_buttons.addButton(self.day_button_60)
        self.day_buttons.addButton(self.day_button_100)

        self.day_buttons.buttonClicked.connect(self.change_num_days)

        self.buttons_widget = qtw.QWidget()
        buttons_layout = qtw.QHBoxLayout()
        buttons_layout.addWidget(self.day_button_30)
        buttons_layout.addWidget(self.day_button_60)
        buttons_layout.addWidget(self.day_button_100)
        self.buttons_widget.setLayout(buttons_layout)

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.hist_box_widget = FigureCanvasQTAgg(self.fig)

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.hist_box_widget)
        layout.addWidget(self.buttons_widget)
        self.setLayout(layout)

        self.draw_box_hist()

    def draw_box_hist(self):
        self.ax.clear()
        
        if self.ax_box:
            self.ax_box.remove()
            self.ax_box = None

        self.ax_box = self.ax.twinx()
        create_mini_hist_box(self.days, self.ax, self.ax_box)

        self.hist_box_widget.draw() 

    def change_num_days(self, button):
        self.days = self.buttons_dict[button.text()]
        self.draw_box_hist()


class MiniTableTab(qtw.QWidget):
    def __init__(self):
        super().__init__()

        mini_df = mini_table()
        table_widget = TableWidget(mini_df, ["Time","Date","Day"])

        layout = qtw.QVBoxLayout()

        layout.addWidget(table_widget)
        self.setLayout(layout)


class MiniTab(qtw.QWidget):
    def __init__(self):
        super().__init__()

        layout = qtw.QVBoxLayout()
        tab_widget = qtw.QTabWidget()

        self.graphs_tab = MiniGraphTab()
        self.tables_tab = MiniTableTab()

        tab_widget.addTab(self.graphs_tab, "Graphs")
        tab_widget.addTab(self.tables_tab, "Table View")

        layout.addWidget(tab_widget)
        self.setLayout(layout)


class TableWidgetConfigure(QAbstractTableModel):
    def __init__(self, dataframe, col_names):
        super().__init__()
        self.dataframe = dataframe
        self.col_names = col_names

    def rowCount(self, parent = None):
        return self.dataframe.shape[0]

    def columnCount(self, parent = None):
        return self.dataframe.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            value = self.dataframe.iloc[index.row(), index.column()]
            return str(value)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.col_names[section]
            elif orientation == Qt.Vertical:
                return str(self.dataframe.index[section])
        return None
    
    def updateData(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()


class TableWidget(qtw.QWidget):
    def __init__(self, dataframe, col_names):
        super().__init__()
        self.dataframe = dataframe

        self.table = qtw.QTableView()
        self.model = TableWidgetConfigure(self.dataframe, col_names)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(qtw.QHeaderView.Stretch)
        

        layout = qtw.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)


class BonusTab(qtw.QWidget):
    def __init__(self):
        super().__init__()

        bonus_df = bonus_table()
        table_widget = TableWidget(bonus_df, ["Time", "Title", "Print Date"])

        layout = qtw.QVBoxLayout()

        layout.addWidget(table_widget)
        self.setLayout(layout)


class RefreshButton(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.get_last_date()

        self.refresh_button = qtw.QPushButton("Refresh Data")
        self.refresh_button.clicked.connect(self.refresh_data)

        layout = qtw.QHBoxLayout()
        layout.addWidget(self.refresh_button)
        self.setLayout(layout)

    def refresh_data(self):
        if self.check_date():
            src.data_refresh.main()
            return
        else:
            if self.confirm_refresh():
                src.data_refresh.main()
                return
            else:
                return
            
    def get_last_date(self):
        with open("data/user_data.json", 'r') as file:
            self._user_data = json.load(file)
        self.last_date = datetime.strptime(self._user_data["last_refresh_date"], "%Y-%m-%d").date()

    def check_date(self):
        if ((date.today() - timedelta(days=1)) - self.last_date).days > 30:
            return False
        return True

    def confirm_refresh(self):
        confirm_window = ConfirmRefresh()
        if confirm_window.exec() == qtw.QMessageBox.Yes:
            return True
        return False        


class ConfirmRefresh(YesNoPopUpWindow):
    def __init__(self):
        text = "It has been more than 30 days since you last refreshed your crossword data. It may take a couple of minutes to refresh. Do you want to proceed?"
        super().__init__("Confirm Data Refresh", text)


class InitalLoadData(qtw.QWidget):
    def __init__(self):
        super().__init__()

        daily_box_layout = qtw.QHBoxLayout()
        self.daily_box_label = qtw.QLabel("Daily Puzzles Start Date: ")
        self.daily_date_box = qtw.QLineEdit()
        self.daily_date_box.setPlaceholderText("YYYY-MM-DD")
        self.daily_date_box.setFixedSize(400, 40)
        daily_box_layout.addWidget(self.daily_box_label)
        daily_box_layout.addWidget(self.daily_date_box)

        mini_box_layout = qtw.QHBoxLayout()
        self.mini_box_label = qtw.QLabel("Mini Puzzles Start Date: ")
        self.mini_date_box = qtw.QLineEdit()
        self.mini_date_box.setPlaceholderText("YYYY-MM-DD")
        self.mini_date_box.setFixedSize(400, 40)
        mini_box_layout.addWidget(self.mini_box_label)
        mini_box_layout.addWidget(self.mini_date_box)

        bonus_box_layout = qtw.QHBoxLayout()
        self.bonus_box_label = qtw.QLabel("Bonus Puzzles Start Date: ")
        self.bonus_date_box = qtw.QLineEdit()
        self.bonus_date_box.setPlaceholderText("YYYY-MM-DD")
        self.bonus_date_box.setFixedSize(400, 40)
        bonus_box_layout.addWidget(self.bonus_box_label)
        bonus_box_layout.addWidget(self.bonus_date_box)

        date_inputs_layout = qtw.QVBoxLayout()
        date_inputs_layout.addLayout(daily_box_layout)
        date_inputs_layout.addLayout(mini_box_layout)
        date_inputs_layout.addLayout(bonus_box_layout)
        
        self.puzzle_type_label = qtw.QLabel(" ")
        self.progress_label = qtw.QLabel(" ")

        self.progress_bar = qtw.QProgressBar()
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(50)

        self.load_button = qtw.QPushButton("Load My Data")
        self.load_button.clicked.connect(self.load_data)

        layout = qtw.QVBoxLayout()
        layout.addLayout(date_inputs_layout)
        layout.addWidget(self.puzzle_type_label, alignment = Qt.AlignCenter)
        layout.addWidget(self.progress_label, alignment = Qt.AlignCenter)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.load_button)

        self.setLayout(layout)

    def load_data(self):
        try:
            with open("data/user_data.json", 'r') as file:
                    data = json.load(file)
            cookies = {"NYT-S": data["cookie"]}

            daily_date = self.daily_date_box.text()
            mini_date = self.mini_date_box.text()
            bonus_date = self.mini_date_box.text()

            self.puzzle_type_label.setText(f"Loading daily puzzles...")
            self.progress_bar.setValue(10)
            self.progress_label.setText("Retrieving puzzle IDs...")
            my_daily_stats, daily_metadata = retrieve_data("daily", daily_date, cookies)
            self.progress_bar.setValue(17)

            self.progress_label.setText("Getting your stats...")
            daily_stats_frame = create_stats_frame(my_daily_stats)
            self.progress_bar.setValue(25)
            
            self.progress_label.setText("Merging stats with metadata...")
            daily_crosswords = merge_frames(daily_stats_frame, daily_metadata)
            daily_crosswords = add_days(daily_crosswords)
            self.progress_bar.setValue(30)

            save_crosswords(daily_crosswords, "daily", daily_date)

            self.puzzle_type_label.setText(f"Loading mini puzzles...")
            self.progress_bar.setValue(37)

            self.progress_label.setText("Retrieving puzzle IDs...")
            my_mini_stats, mini_metadata = retrieve_data("mini", mini_date, cookies)
            self.progress_bar.setValue(45)

            self.progress_label.setText("Getting your stats...")
            mini_stats_frame = create_stats_frame(my_mini_stats)
            self.progress_bar.setValue(50)
            
            self.progress_label.setText("Merging stats with metadata...")
            mini_crosswords = merge_frames(mini_stats_frame, mini_metadata)
            mini_crosswords = add_days(mini_crosswords)
            self.progress_bar.setValue(60)

            save_crosswords(mini_crosswords, "mini", mini_date)

            self.puzzle_type_label.setText(f"Loading bonus puzzles...")
            self.progress_bar.setValue(67)

            self.progress_label.setText("Retrieving puzzle IDs...")
            my_bonus_stats, bonus_metadata = retrieve_data("bonus", bonus_date, cookies)
            self.progress_bar.setValue(75)

            self.progress_label.setText("Getting your stats...")
            bonus_stats_frame = create_stats_frame(my_bonus_stats)
            self.progress_bar.setValue(85)
            
            self.progress_label.setText("Merging stats with metadata...")
            bonus_crosswords = merge_frames(bonus_stats_frame, bonus_metadata)
            bonus_crosswords = add_days(bonus_crosswords)
            self.progress_bar.setValue(95)
            
            save_crosswords(bonus_crosswords, "bonus", bonus_date)
            self.progress_label.setText("Data load is complete!")

            data["last_refreshed_data"] = str(date.today() - timedelta(days=1))
 
            with open('data/user_data.json', 'w') as f:
                json.dump(data, f)

        except Exception as e:
            self.puzzle_type_label.setText("There was an error getting your data. Please check your cookie and internet connection")

        main_window = MainWindow()
        main_window.show()
        self.close()

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1000, 600)
        layout = qtw.QHBoxLayout()
        self.setLayout(layout)

        self.left_panel = qtw.QWidget()
        left_panel_layout = qtw.QVBoxLayout()

        self.left_panel_top = qtw.QListWidget()

        self.left_panel_top.addItem("Daily")
        self.left_panel_top.addItem("Mini")
        self.left_panel_top.addItem("Bonus")

        self.left_panel_top.currentRowChanged.connect(self.change_page)
        
        self.left_panel_pages = qtw.QStackedWidget()
        daily = DailyTab()
        mini = MiniTab()
        bonus = BonusTab()
        
        self.left_panel_pages.addWidget(daily)
        self.left_panel_pages.addWidget(mini)
        self.left_panel_pages.addWidget(bonus)

        left_panel_layout.addWidget(self.left_panel_top)

        self.refresh_button = RefreshButton()
        left_panel_layout.addWidget(self.refresh_button)

        self.left_panel.setLayout(left_panel_layout)

        layout.addWidget(self.left_panel, 1)
        layout.addWidget(self.left_panel_pages, 4)
        
        self.left_panel_top.setCurrentRow(0)

    def change_page(self, index):
        self.left_panel_pages.setCurrentIndex(index)