from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
import os
import re
from shutil import copyfile

class GUI(App):
    def build(self):
        return Builder.load_file("GUI.kv")
class WindowManager(ScreenManager):
    """ manage transitions between screens and other properties """
    pass

#self.filechooser.selection -> list of selected files\dirs


class CheckDeletePopUp(Widget):
    pass
class MainScreen(Screen):
    def __init__(self, **kwargs):
        # IDs for kv file widgets and needed values
        super(Screen, self).__init__(**kwargs)#init screen
        #############################################################
        ###objects reffering to id's of widgets in the GUI.kv file###
        #############################################################
        self.path_in=ObjectProperty(None)
        self.filter_in=ObjectProperty(None)
        self.filechooser=ObjectProperty(None)
        self.in_selected=ObjectProperty(None)
        self.in_changeExtension=ObjectProperty(None)
        self.in_addPrefix=ObjectProperty(None)
        self.in_copy=ObjectProperty(None)
        self.popup=None
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
            self.filechooser.filters=[self.Filter]
    def insert_selected(self):
        ################################################################
        #insert files in the selection textbox into filechooser list   #
        #of selected files in the current working directory.           #
        #in case of files in sub directories, their path               #
        #from the working directory should be written.                 #
        ################################################################
        filesText = self.in_selected.text   #get text from textbox
        if filesText=="":
            self.filechooser.selection=[]
            return
        filesList = filesText.split(',')
        collection=[]       #will contain the files names in unicode.
        for fileText in filesList:
            #the strip method removes any whitespace character form the edges.
            fileText=fileText.strip()
            fullpath=self.filechooser.path +'\\'+ fileText
            if (not os.path.isfile(fullpath)):
                self.in_selected.text="invalid input. \""+fullpath
                self.in_selected.text+="\" doesn't exist"
                return False
            collection.append(unicode(self.filechooser.path +fileText))
            #selection is a list of unicodes


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
            word=word.replace(self.filechooser.path,"")
            if ((word[0]=='\\') or (word[0]=='/')):
                word=word[1:]  #"\\" and "/" can stand for "root"
            filesView+=word +" , "
        filesView=filesView[:-3]#fix of the lest " , " character
        self.in_selected.text=filesView #insert the text to the textbox


    def Changeextension(self):
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
        self.filechooser.path=dirpath      #makes sure we stay at the same path
        self.in_changeExtension.text="please insert new extension here"
        self.update_selected()


    def AddPrefix(self):
        #add extension to all selected files
        collection =self.filechooser.selection
        dirpath=self.filechooser.path
        if len(collection)==0:return
        if collection[0]==dirpath:collection=collection[1:]
        for path in collection:
            pathbackup=path
            prefix=self.in_addPrefix.text  #new extension
            i = 0
            index=path.rfind('\\')+1
            #new file full path (including the prefix)
            npath=path[:index] + prefix + path[index:]
            if (os.path.isfile(npath)):
                #in case it's occupied. add (0)
                dotindex=npath.rfind('.')
                npath+=npath[:dotindex]+"("+str(i)+")"+npath[dotindex:]
                #if still occupied
                while (os.path.isfile(npath)):
                    #replace older fix
                    i+=1
                    npath=npath[:path.rfind('(')+1]+str(i)
                    +npath[npath.rfind(')'):]
            os.rename(pathbackup,npath)
            #update change in collection
            collection[collection.index(pathbackup)]=npath
        self.filechooser._update_files()    #refresh the listview
        self.filechooser.path=dirpath
        self.in_addPrefix.text="please insert new prefix here"
        self.update_selected()      #update selected files in textinput
    def Copy(self):
        newPath=self.in_copy.text
        #if the path isn't valid
        if (not os.path.isdir(newPath)):
            self.in_copy.text="dir doesn't exist! please insert path here"
            return
        collection =self.filechooser.selection
        if len(collection)==0:return
        if collection[0]==self.filechooser.path:collection=collection[1:]
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
        self.filechooser._update_files()    #refresh the listview
    def CheckDelete(self):
        #confirm that the user want to delete the selected files.
        show = CheckDeletePopUp()
        #bind functions to buttons of CheckDeletePopUp.
        show.ids["Confirm"].on_release=self.Delete
        show.ids["Cancel"].on_release=self.CancelPopUp
        #create popup
        self.popup=Popup(title="Confirmation",content=show,
        size_hint=(None,None),size=(500,300))
        self.popup.open()
    def CancelPopUp(self):
        #close the popup window
        self.popup.dismiss()
    def Delete(self):
        #close popup window and delete files
        self.popup.dismiss()
        for path in self.filechooser.selection:
            os.remove(path)
        #refresh the filechooser and selection textinput and list
        self.filechooser._update_files()    #refresh the listview
        self.filechooser.selection=[]
        self.in_selected.text=""
        #regex filter , used as callback function for the filechooser filter
    def Filter(self, folder, name):
        if re.findall(self.filter_in.text,name) !=[]:
            return True
        return False

if __name__ == '__main__':
    GUI().run()
