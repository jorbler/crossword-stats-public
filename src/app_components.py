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
    '''Creates a dialog box with title, body text, and Yes/No buttons.'''
    def __init__(self, title: str, body_text: str) -> None:
        super().__init__()
        
        self.setWindowTitle(title)
        self.setText(body_text)
        self.setStandardButtons(qtw.QMessageBox.Yes | qtw.QMessageBox.No)
        self.setDefaultButton(qtw.QMessageBox.Yes)
        self.setFont(QFont("Arial", 14, weight = 1))


class WelcomeWindow(YesNoPopUpWindow):
    '''Welcome window that appears to the user the first time that they open the app.'''
    def __init__(self) -> None:
        intro_text = "Welcome to MyCrosswordBuddy! This app allows you to gain insight into your NYT Crossword data. \nTo access your data, you will need to enter the cookie associated with your NYT Games account.\n\nDo you need instructions on how to access your cookie?"
        super().__init__("Welcome!", intro_text)


class MenuPage(qtw.QWidget):
    '''QWidget containing text and an optional image.'''
    def __init__(self, text: str, rel_image_path: str = None) -> None:
        super().__init__()
        layout = qtw.QVBoxLayout()
        layout.addWidget(qtw.QLabel(text))

        if rel_image_path:
            page_image = qtw.QLabel()
            page_image.setPixmap(QPixmap(os.getcwd() + rel_image_path))
            layout.addWidget(page_image)
        self.setLayout(layout)


class IntroMenuPages(qtw.QWidget):
    '''Menu that has next and previous arrows that switch the "page" of the menu.'''
    def __init__(self) -> None:
        super().__init__()
        self.create_pages()
        self.setWindowTitle("Cookie Instructions")
        self.resize(400, 300)
        self.show()
    
    def create_pages(self) -> None:
        '''Creates a stacked widget containing all of the menu pages and adds the next and previous buttons'''
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

    def next_page(self) -> None:
        '''Go to next page in a stacked widget'''
        cur_index = self.stacked_widget.currentIndex()
        if cur_index < self.stacked_widget.count() -1:
            self.stacked_widget.setCurrentIndex(cur_index + 1)
        self.update_buttons()
    
    def prev_page(self) -> None:
        '''Go to previous page in a stacked widget'''
        cur_index = self.stacked_widget.currentIndex()
        if cur_index > 0:
            self.stacked_widget.setCurrentIndex(cur_index - 1)
        self.update_buttons()

    def update_buttons(self) -> None:
        '''Change button states based on the current index'''
        cur_index = self.stacked_widget.currentIndex()
        total_pages = self.stacked_widget.count()

        self.prev_button.setEnabled(cur_index > 0)
        self.next_button.setEnabled(cur_index < (total_pages - 1))


class EnterCookie(qtw.QDialog):
    '''A popup window that prompts the user to enter their cookie into a text box.'''
    def __init__(self) -> None:
        super().__init__()
        print("in EnterCookie widget")
        self.setWindowTitle('Welcome!')

        self.welcome_text = qtw.QLabel("Welcome to MyCrosswordBuddy! This app allows you to gain insight into your NYT Crossword data. \nTo access your data, you will need to enter the cookie associated with your NYT Games account.\n\nFor detailed instructions on how to access your cookie, please go to the README file.")        

        self.input_box = qtw.QLineEdit()
        self.input_box.setPlaceholderText("Enter your cookie here")
        self.input_box.setFixedSize(400, 40)

        self.ok_button = qtw.QPushButton("OK", self)

        self.ok_button.clicked.connect(self.save_cookie)
        
        self.my_layout = qtw.QVBoxLayout(self)
        self.my_layout.addWidget(self.welcome_text)
        self.my_layout.addWidget(self.input_box)
        self.my_layout.addWidget(self.ok_button)
        
    def save_cookie(self) -> None:
        '''Grabs text from input box and assigns user cookie to self.cookie.'''
        self.cookie_value = self.input_box.text()
        user_dict = {"cookie":self.cookie_value}
        with open('data/user_data.json', 'w') as f:
            json.dump(user_dict, f)
        self.init_load = InitalLoadData()
        self.init_load.show()
        self.accept()


class DailyHistTab(qtw.QWidget):
    '''QWidget containing the histograms for the daily crosswords.'''
    def __init__(self) -> None:
        super().__init__()
        self.day = "Monday"

        #days_in_data = 

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

    def draw_hist(self) -> None:
        '''Clear the axis and draw the histogram'''
        self.ax.clear()
        create_hist(self.day, self.ax)
        self.hist_widget.draw() 

    def text_changed(self, s: str) -> None:
        '''Change self.day to the day that the user selects in the combo box.'''
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
    '''QWidget containing a stacked widget with DailyHistTab and DailyBarTab.'''
    def __init__(self) -> None:
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
    '''QWidget that contains a table showing daily stats.'''
    def __init__(self) -> None:
        super().__init__()

        daily_df = daily_table()
        table_widget = TableWidget(daily_df, ["Time","Date","Day"])

        layout = qtw.QVBoxLayout()

        layout.addWidget(table_widget)
        self.setLayout(layout)


class DailyTab(qtw.QWidget):
    '''QWidget containing DailyTableTab and DailyGraphsTab'''
    def __init__(self) -> None:
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
    '''QWidget containing graphs for mini data.'''
    def __init__(self) -> None:
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

    def draw_box_hist(self) -> None:
        '''Clears axes and draws graph.'''
        self.ax.clear()
        
        if self.ax_box:
            self.ax_box.remove()
            self.ax_box = None

        self.ax_box = self.ax.twinx()
        create_mini_hist_box(self.days, self.ax, self.ax_box)

        self.hist_box_widget.draw() 

    def change_num_days(self, button: qtw.QButtonGroup) -> None:
        '''Change self.days the number that corresponds to the button that the user pushes.'''
        self.days = self.buttons_dict[button.text()]
        self.draw_box_hist()


class MiniTableTab(qtw.QWidget):
    '''QWidget containing table for mini data.'''
    def __init__(self) -> None:
        super().__init__()

        mini_df = mini_table()
        table_widget = TableWidget(mini_df, ["Time","Date","Day"])

        layout = qtw.QVBoxLayout()

        layout.addWidget(table_widget)
        self.setLayout(layout)


class MiniTab(qtw.QWidget):
    '''QWidget containing MiniGraphTab and MiniTableTab'''
    def __init__(self) -> None:
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
    '''Configures table from a Pandas DataFrame.'''
    def __init__(self, dataframe: pd.DataFrame, col_names: list[str]) -> None:
        super().__init__()
        self.dataframe = dataframe
        self.col_names = col_names

    def rowCount(self, parent = None) -> int:
        return self.dataframe.shape[0]

    def columnCount(self, parent = None) -> int:
        return self.dataframe.shape[1]

    def data(self, index, role=Qt.DisplayRole) -> None:
        if role == Qt.DisplayRole:
            value = self.dataframe.iloc[index.row(), index.column()]
            return str(value)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole) -> None:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.col_names[section]
            elif orientation == Qt.Vertical:
                return str(self.dataframe.index[section])
        return None


class TableWidget(qtw.QWidget):
    '''Creates QWidget containing table from TableWidgetConfigure.'''
    def __init__(self, dataframe:pd.DataFrame, col_names:list[str]) -> None:
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
    '''QWidget containing data for bonus puzzles.'''
    def __init__(self) -> None:
        super().__init__()

        bonus_df = bonus_table()
        table_widget = TableWidget(bonus_df, ["Time", "Title", "Print Date"])

        layout = qtw.QVBoxLayout()

        layout.addWidget(table_widget)
        self.setLayout(layout)


class RefreshButton(qtw.QWidget):
    '''QWidget containing a QPushButton that triggers the data refresh process.'''
    def __init__(self):
        super().__init__()
        self.get_last_date()

        self.refresh_button = qtw.QPushButton("Refresh Data")
        self.refresh_button.clicked.connect(self.refresh_data)

        layout = qtw.QHBoxLayout()
        layout.addWidget(self.refresh_button)
        self.setLayout(layout)

    def refresh_data(self) -> None:
        '''Events triggered by pressing "Refresh Data" button.'''
        if self.check_date():
            src.data_refresh.main()
            return
        else:
            if self.confirm_refresh():
                src.data_refresh.main()
                return
            else:
                return
            
    def get_last_date(self) -> None:
        '''Retrieves the last date from the user_data.json file.'''
        with open("data/user_data.json", 'r') as file:
            self._user_data = json.load(file)
        self.last_date = datetime.strptime(self._user_data["last_refresh_date"], "%Y-%m-%d").date()

    def check_date(self) -> bool:
        '''Checks if the last date of refresh (self.last_date) was more than 30 days ago.'''
        if ((date.today() - timedelta(days=1)) - self.last_date).days > 30:
            return False
        return True

    def confirm_refresh(self) -> bool:
        '''Opens pop-up window that confirms that the user wants to proceed with refreshing data.'''
        confirm_window = ConfirmRefresh()
        if confirm_window.exec() == qtw.QMessageBox.Yes:
            return True
        return False        


class ConfirmRefresh(YesNoPopUpWindow):
    '''YesNoPopUpWindow informing user that it has been more than 30 days since last data refresh and confirming that they want to proceed.'''
    def __init__(self) -> None:
        text = "It has been more than 30 days since you last refreshed your crossword data. It may take a couple of minutes to refresh. Do you want to proceed?"
        super().__init__("Confirm Data Refresh", text)


class InitalLoadData(qtw.QDialog):
    '''
    Loads the all of the initial user data upon first opening the app.
    Asks user for start dates for each puzzle type.
    '''
    def __init__(self) -> None:
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
        self.progress_bar.setValue(1)

        self.load_button = qtw.QPushButton("Load My Data")
        self.load_button.clicked.connect(self.load_data)

        self.continue_button = qtw.QPushButton("Continue", self)
        self.continue_button.clicked.connect(self.show_main_window)
        self.continue_button.setEnabled(False)

        buttons_layout = qtw.QHBoxLayout()
        buttons_layout.addWidget(self.load_button)
        buttons_layout.addWidget(self.continue_button)

        layout = qtw.QVBoxLayout()
        layout.addLayout(date_inputs_layout)
        layout.addWidget(self.puzzle_type_label, alignment = Qt.AlignCenter)
        layout.addWidget(self.progress_label, alignment = Qt.AlignCenter)
        layout.addWidget(self.progress_bar)
        layout.addLayout(buttons_layout)
        

        self.setLayout(layout)

    def load_data(self) -> None:
        '''Loads user data.'''
        try:
            with open("data/user_data.json", 'r') as file:
                    data = json.load(file)
            cookies = {"NYT-S": data["cookie"]}

            daily_date = self.daily_date_box.text()
            mini_date = self.mini_date_box.text()
            bonus_date = self.mini_date_box.text()

            print(f"Loading daily puzzles...")
            self.progress_bar.setValue(10)
            qtw.QApplication.processEvents()
            print("Retrieving puzzle IDs...")
            my_daily_stats, daily_metadata = retrieve_data("daily", daily_date, cookies)
            self.progress_bar.setValue(17)
            qtw.QApplication.processEvents()

            print("Getting your stats...")
            qtw.QApplication.processEvents()
            daily_stats_frame = create_stats_frame(my_daily_stats)
            self.progress_bar.setValue(25)
            qtw.QApplication.processEvents()
            
            print("Merging stats with metadata...")
            daily_crosswords = merge_frames(daily_stats_frame, daily_metadata)
            daily_crosswords = add_days(daily_crosswords)
            self.progress_bar.setValue(30)

            save_crosswords(daily_crosswords, "daily", daily_date)

            print(f"Loading mini puzzles...")
            self.progress_bar.setValue(37)
            qtw.QApplication.processEvents()

            print("Retrieving puzzle IDs...")
            my_mini_stats, mini_metadata = retrieve_data("mini", mini_date, cookies)
            self.progress_bar.setValue(45)
            qtw.QApplication.processEvents()

            print("Getting your stats...")
            mini_stats_frame = create_stats_frame(my_mini_stats)
            self.progress_bar.setValue(50)
            qtw.QApplication.processEvents()

            print("Merging stats with metadata...")
            mini_crosswords = merge_frames(mini_stats_frame, mini_metadata)
            mini_crosswords = add_days(mini_crosswords)
            self.progress_bar.setValue(60)
            qtw.QApplication.processEvents()

            save_crosswords(mini_crosswords, "mini", mini_date)

            print(f"Loading bonus puzzles...")
            self.progress_bar.setValue(67)
            qtw.QApplication.processEvents()

            print("Retrieving puzzle IDs...")
            my_bonus_stats, bonus_metadata = retrieve_data("bonus", bonus_date, cookies)
            self.progress_bar.setValue(75)
            qtw.QApplication.processEvents()

            print("Getting your stats...")
            bonus_stats_frame = create_stats_frame(my_bonus_stats)
            self.progress_bar.setValue(85)
            qtw.QApplication.processEvents()
            
            print("Merging stats with metadata...")
            bonus_crosswords = merge_frames(bonus_stats_frame, bonus_metadata)
            bonus_crosswords = add_days(bonus_crosswords)
            self.progress_bar.setValue(95)
            qtw.QApplication.processEvents()
            
            save_crosswords(bonus_crosswords, "bonus", bonus_date)
            
            data["last_refresh_date"] = str(date.today() - timedelta(days=1))
 
            with open('data/user_data.json', 'w') as f:
                json.dump(data, f)
            
            self.continue_button.setEnabled(True)
            self.load_button.setEnabled(False)
            self.progress_label.setText("Data load is complete! Please click 'continue'")

        except Exception as e:
            self.puzzle_type_label.setText("There was an error getting your data. Please check your cookie and internet connection")

    def show_main_window(self) -> None:
        '''Shows main window and accepts current window.'''
        self.main_window = MainWindow()
        self.main_window.show()
        self.accept()


class MainWindow(qtw.QWidget):
    '''Main window containing DailyTab, MiniTab, and BonusTab, along with a left navigation panel.'''
    def __init__(self) -> None:
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

    def change_page(self, index: int) -> None:
        '''Changes page to index of the QListWidget.'''
        self.left_panel_pages.setCurrentIndex(index)