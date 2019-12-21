from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty


class GUI(App):
    def build(self):
        return Builder.load_file("GUI.kv")
class WindowManager(ScreenManager):
    """ manage transitions between screens and other properties """
    pass
class MainScreen(Screen):
    def __init__(self, **kwargs):
        # IDs for kv file widgets and needed values
        super(Screen, self).__init__(**kwargs)
        self.cpath= ObjectProperty(None)



def main():
    pass

if __name__ == '__main__':
    GUI().run()
