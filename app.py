from src.app_components import *
from PyQt5 import QtWidgets as qtw
import sys

class SimpleApp(qtw.QApplication):
    '''
    Contains a VerticalHelloBox to
    prompt the user for their name and say hello!
    '''
    def __init__(self, **kwargs):
        super().__init__([])

        # Add the VerticalHelloBox
        self.main_widget = WelcomeWindow()

        # Run the application
        self.main_widget.show()
        sys.exit(self.exec_())
        return

class WindowWithVerticalSlots(qtw.QWidget):
    '''
    A window with a title and an empty
    vertical container (QVBoxLayout).
    
    Intended use is to inherit and add
    additional customization
    '''
    def __init__(self, title: str):
        super().__init__()
        
        # Make a title for the window
        self.setWindowTitle(title)
        
        # Create an empty vertical layout container
        self.my_layout = qtw.QVBoxLayout(self)
        return

class WelcomeWindow(WindowWithVerticalSlots):
    '''
    Contains a textbox and a button the user can
    press which opens up another window for them to
    enter their name
    '''
    def __init__(self):
        super().__init__(title = "Welcome!")
        self.configure()
        return
    
    def configure(self):
        self.greeting_box = qtw.QLabel(self)
        self.hello_button = qtw.QPushButton('Who are you?', self)
        
        # Bind the hello_button_clicked function to 
        # the clicked event of the hello_button
        self.hello_button.clicked.connect(self.hello_button_clicked)
        
        # Add the widgets to the layout
        self.my_layout.addWidget(self.greeting_box)
        self.my_layout.addWidget(self.hello_button)
        return
    
    def hello_button_clicked(self):
        # Create a new input popup
        name_getter = InputPopup('Who are you?')

        # This runs the dialog box and waits for the user to click
        # the ok button.
        if name_getter.exec_() == qtw.QDialog.Accepted:
            # Update the text in the main window with the text entered
            # by the user
            self.greeting_box.setText(f'Hello {name_getter.get_text()}!')
        return
    
class InputPopup(qtw.QDialog):
    '''
    A popup window with a text box and an OK button
    to allow a user to enter some freeform text.
    '''
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)

        # Text box to enter your name
        self.name_entry = qtw.QLineEdit(self)

        # Button to click when you are done entering your name
        self.ok_button = qtw.QPushButton("Ok", self)

        # When the button is clicked, calls the accept()
        # method of the QDialog, which lets the app know
        # that the interaction with the dialog is complete
        self.ok_button.clicked.connect(self.accept)
        
        # Create a vertical layout and add the widgets
        self.my_layout = qtw.QVBoxLayout(self)
        self.my_layout.addWidget(self.name_entry)
        self.my_layout.addWidget(self.ok_button)
        return
    
    def get_text(self) -> str:
        # Get the name that was entered into the text box
        return self.name_entry.text()

if __name__ == '__main__':
    SimpleApp()