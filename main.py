from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
import os

class GUI(App):
    def build(self):
        return Builder.load_file("GUI.kv")
class WindowManager(ScreenManager):
    """ manage transitions between screens and other properties """
    pass

#self.filechooser.files -> list of files the fileschooser display
#self.filechooser.selection -> list of selected files\dirs



class MainScreen(Screen):
    def __init__(self, **kwargs):
        # IDs for kv file widgets and needed values
        super(Screen, self).__init__(**kwargs)
        self.path_in=ObjectProperty(None)
        self.filter_in=ObjectProperty(None)
        self.filechooser=ObjectProperty(None)
        self.in_selected=ObjectProperty(None)
    def insert_path(self):
        path = self.path_in.text
        if (len(path)==2 and path[-1]==':'):
            path+="\\"
        if (os.path.isdir(path)):
            self.filechooser.path=path
        else:
            self.path_in.text="path isn't valid!"
    def insert_filter(self):
        if self.filter_in.text=="":
            self.filechooser.filters=[]
        else:
            self.filechooser.filters=[self.filter_in.text]
    def insert_selected(self):
        try:
            l = eval(self.in_selected.text)
            if type(l)==list():
                self.filechooser.selection=eval()
            else:
                self.in_selected.text="input is invalid!"
        except:
            self.in_selected.text="input is invalid!"
    #def update_selected(self):
        #updates the selected files textbox.
        #self.in_selected.text=self.filechooser.selection
def main():
    pass

if __name__ == '__main__':
    GUI().run()
