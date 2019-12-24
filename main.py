from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
import os
from shutil import copyfile

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
        super(Screen, self).__init__(**kwargs)#init screen
        #########################################################
        #objects reffering to id's of widgets in the GUI.kv file#
        #########################################################
        self.path_in=ObjectProperty(None)
        self.filter_in=ObjectProperty(None)
        self.filechooser=ObjectProperty(None)
        self.in_selected=ObjectProperty(None)
        self.in_changeExtension=ObjectProperty(None)
        self.in_addExtension=ObjectProperty(None)
        self.in_copy=ObjectProperty(None)
    def insert_path(self):
        #takes path from textbox
        path = self.path_in.text
        #in case of input pattern "X:"
        if (len(path)==2 and path[-1]==':'):
            path+="\\"
        #check if path is valid. if it's valid, go to path.
        if (os.path.isdir(path)):
            self.filechooser.path=path
        elif (os.path.isfile(path)):
            self.path_in.text="path should point into a directory!"
        else:
            self.path_in.text="path does'nt exist!"
    def insert_filter(self):
        #uses kivy filechooser filter.
        if self.filter_in.text=="":
            #if its blank, there is no fiter
            self.filechooser.filters=[]
        else:
            # the character '*' represent all cheracters
            self.filechooser.filters=["*"+self.filter_in.text+"*"]
    def insert_selected(self):
        ################################################################
        #insert files in the selection textbox into filechooser list   #
        #of selected files in the current working directory.           #
        #in case of files in sub directories, their path               #
        #from the working directory should be written.                 #
        ################################################################
        filesText = self.in_selected.text   #get text from textbox
        filesList = filesText.split(',')
        collection=[]       #will contain the files names in unicode.
        for fileText in filesList:
            #the strip method removes any whitespace character form the edges.
            fileText=fileText.strip()
            if (not os.path.isfile(self.filechooser.path + fileText)):
                self.in_selected.text="invalid input. "+fileText+" doesn't exist"
                return False
            collection.append(unicode(self.filechooser.path +fileText))
            #selection is a list of unicodes
        self.filechooser.selection=collection


    def update_selected(self):
        #updates the selected files textbox.
        filesView=""
        collection =self.filechooser.selection
        #in case the collection is empty
        if len(collection)==0:
            self.in_selected.text=""
            return
        #because the firstargument may be the current path:
        if collection[0]==self.filechooser.path:collection=collection[1:]
        for word in collection:#collection of chosen files
            #remove the path from the files names.
            if word[0]=='\\':word=word[1:]  #"\\" and "/" can stand for "root"
            filesView+=word.replace(self.filechooser.path,"") + " , "
        filesView=filesView[:-3]#fix of the lest " , " character
        self.in_selected.text=filesView #insert the text to the textbox


    def ChangeExtansion(self):
    #changes the whole extensions of all selected files
        collection =self.filechooser.selection
        dirpath=self.filechooser.path
        if len(collection)==0:return
        if collection[0]==dirpath:collection=collection[1:]
        for path in collection:
            pathbackup=path
            index=path.find('.') #find '.' index
            path=path[:index]
            extension=self.in_changeExtension.text  #new extension
            if extension[0]!='.':extension='.'+extension    #fix
            i = 0
            #if occupied
            if (os.path.isfile(path+extension)):
                path+="("+str(i)+")"
                #if occupied
                while (os.path.isfile(path+extension)):
                    #replace older fix
                    path=path[:path.rfind('(')]
                    i+=1
                    path+="("+str(i)+")"
            os.rename(pathbackup,path+extension)
            #update change in collection
            collection[collection.index(pathbackup)]=path+extension
        self.filechooser._update_files()    #refresh the listview
        self.filechooser.path=dirpath
        self.in_changeExtension.text="please insert new extansion here"
        self.update_selected()


    def AddExtansion(self):
        #add extansion to all selected files
        collection =self.filechooser.selection
        dirpath=self.filechooser.path
        if len(collection)==0:return
        if collection[0]==dirpath:collection=collection[1:]
        for path in collection:
            pathbackup=path
            extension=self.in_addExtension.text  #new extension
            if extension[0]!='.':extension='.'+extension    #fix
            i = 0
            #if occupied
            if (os.path.isfile(path+extension)):
                path+="("+str(i)+")"
                #if occupied
                while (os.path.isfile(path+extension)):
                    #replace older fix
                    path=path[:path.rfind('(')]
                    i+=1
                    path+="("+str(i)+")"
            os.rename(pathbackup,path+extension)
            #update change in collection
            collection[collection.index(pathbackup)]=path+extension
        self.filechooser._update_files()    #refresh the listview
        self.filechooser.path=dirpath
        self.in_addExtension.text="please insert new extansion here"
        self.update_selected()
    def Copy(self):
        newPath=self.in_copy.text
        #if the path isn't valid
        if (not os.path.isdir(newPath)):
            self.in_copy.text="dir doesn't exist! please insert path here"
            return
        collection =self.filechooser.selection
        if len(collection)==0:return
        if collection[0]==dirpath:collection=collection[1:]
        for path in collection:
            name = path[path.rfind("\\")+1:]    #extracts name from path
            npath=newPath+"\\"+name
            i = 0
            #if occupied
            if (os.path.isfile(npath)):
                npath+="("+str(i)+")"
                #if occupied
                while (os.path.isfile(npath)):
                    #replace older fix
                    npath=npath[:npath.rfind('(')]
                    i+=1
                    npath+="("+str(i)+")"
            copyfile(path,npath)
        #note: should go to the new path or not ?
    def CheckDelete(self):
        pass
    #implement popupwindow and then call Delete()
    def Delete(self):
        pass


def main():
    pass

if __name__ == '__main__':
    GUI().run()
