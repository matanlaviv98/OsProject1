from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen



class GUI(App):
    def build(self):
        return Builder.load_file("GUI.kv")
class WindowManager(ScreenManager):
    """ manage transitions between screens and other properties """
    pass
class MainScreen(Screen):
    pass




def main():
    pass

if __name__ == '__main__':
    GUI().run()
