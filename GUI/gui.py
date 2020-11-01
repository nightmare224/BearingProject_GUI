import dash_html_components as html
import dash_core_components as dcc

from GUI.app import app
from GUI.layouts import Layout


class GUI:
    def __init__(self):
        self.app = app
        self.app.config['suppress_callback_exceptions'] = True
        # Create Layout Object
        self.layout = Layout()
        # build Layout
        self.__tabOne__()
        self.__tabTwo__()
        self.__mainPage__()
    def __mainPage__(self):
        # Config the mainpage
        self.layout.setMainPage()
        # Put the Page to app
        self.app.layout = self.layout.mainPage
    def __tabOne__(self):
        self.layout.setTabOne()
    def __tabTwo__(self):
        self.layout.setTabTwo()






        


