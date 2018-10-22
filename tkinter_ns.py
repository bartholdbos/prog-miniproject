from tkinter import *
from infoFunctions import *


def init():
    root = Tk()

    # root.overrideredirect(True)
    # root.overrideredirect(False)
    # root.attributes('-fullscreen', True)

    root.state('zoomed')

    mainContainer = container(root)
    mainContainer.viewInputStationFrame()

    root.mainloop()


class container():

    def __init__(self, master):
        self.inputStationWindow = inputStationWindow(self, master)
        self.showInfoWindow = showInfoWindow(self, master)

    def viewInputStationFrame(self):
        self.showInfoWindow.infoFrame.pack_forget()
        self.inputStationWindow.inputStationFrame.pack()

    def viewInfoFrame(self):
        self.inputStationWindow.inputStationFrame.pack_forget()
        self.showInfoWindow.infoFrame.pack()

    def showinfostation(self, currentStation = False):
        if currentStation:
            station = 'Utrecht'
        else:
            station = self.inputStationWindow.inputField.get()
        self.showInfoWindow.infoLabel["text"] = data(station)
        self.viewInfoFrame()


class inputStationWindow():

    def __init__(self, parent, master):
        self.inputStationFrame = Frame(master=master)
        self.inputStationFrame.pack(fill="both", expand=True)
        self.inputField = Entry(master=self.inputStationFrame)
        self.inputField.pack(padx=20, pady=20)
        self.inputButton = Button(master=self.inputStationFrame, text='vertrektijden station',
                                  command=parent.showinfostation)
        self.inputButton.pack(padx=20, pady=20)


        self.currentButton = Button(master=self.inputStationFrame, text='Huidige station',
                                  command=lambda : parent.showinfostation(True))
        self.currentButton.pack(padx=20, pady=20)

class showInfoWindow():

    def __init__(self, parent, master):
        self.infoFrame = Frame(master=master)
        self.infoFrame.pack(fill="both", expand=True)
        self.infoLabel = Label(master=self.infoFrame, text='')
        self.infoLabel.pack()
        self.backbutton = Button(master=self.infoFrame, text='<', command=parent.viewInputStationFrame)
        self.backbutton.pack(padx=20, pady=20)


init()
