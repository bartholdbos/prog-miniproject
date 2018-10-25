from tkinter import *
from infoFunctions import *
from tkinter import messagebox

def init():

    root = Tk()

    # root.overrideredirect(True)
    # root.overrideredirect(False)
    # root.attributes('-fullscreen', True)

    root.state('zoomed')
    root.configure(bg='#ffc917')
    mainContainer = container(root)
    mainContainer.viewInputStationFrame()

    root.mainloop()

class container():

    def __init__(self, master):
        self.inputStationWindow = inputStationWindow(self, master)
        self.showInfoWindow = showInfoWindow(self, master)



    def viewInputStationFrame(self):

        self.showInfoWindow.infoFrame.pack_forget()
        self.inputStationWindow.inputStationFrame.pack(fill="none", expand=TRUE, ipadx=200, ipady=200)

    def viewInfoFrame(self):

        self.inputStationWindow.inputStationFrame.pack_forget()
        self.showInfoWindow.infoFrame.pack(fill="none", expand=TRUE, ipadx=200, ipady=200)

    def showinfostation(self, currentStation = False):
        if currentStation:
            station = 'Utrecht'
        else:
            station = self.inputStationWindow.inputField.get()
            if station == '':
                messagebox.showerror("Invoerveld leeg", "De invoerveld is leeg")
        self.showInfoWindow.infoLabel["text"] = 'Huidig station: '+station + '\n'
        self.showInfoWindow.infoLabel["text"] += data(station)

        self.viewInfoFrame()
def showbutton():
    messagebox.showerror("Error", "Buiten gebruik zehmeeer")


class inputStationWindow():

    def __init__(self, parent, master):
        self.inputStationFrame = Frame(master=master, width=768, height=576, bg='#ffc917')
        self.inputStationFrame.grid_propagate(False)
        self.inputStationFrame.pack(fill="none", expand=TRUE, ipadx=200, ipady=200)
        self.title = Label(self.inputStationFrame, text="Vul hier uw gewenste station in", height=2)
        self.title.pack()
        self.inputField = Entry(master=self.inputStationFrame)
        self.inputField.pack(pady=20, padx=20)
        self.inputButton = Button(master=self.inputStationFrame, text='vertrektijden station',
                                  command=parent.showinfostation, height=3, bg='#0079d3', fg='white')
        self.inputButton.pack(padx=5, pady=10, side=LEFT, expand=YES)

        self.currentButton = Button(master=self.inputStationFrame, text='Huidige station',
                                  command=lambda : parent.showinfostation(True), height=3, bg='#0079d3', fg='white')
        self.currentButton.pack(padx=5, pady=10, side=LEFT, expand=YES)

        self.tkButton = Button(master=self.inputStationFrame, command=showbutton, state=DISABLED, text='Los kaartje kopen', height=3, bg='#0079d3', fg='white')
        self.tkButton.pack(padx=5, pady=10, side=LEFT, expand=YES)

        self.ovButton = Button(master=self.inputStationFrame, command=showbutton, state=DISABLED, text='Ov-chipkaart opladen', height=3, bg='#0079d3', fg='white')
        self.ovButton.pack(padx=5, pady=10, side=LEFT, expand=YES)
        img = PhotoImage(file='ns1.png')
        self.inputStationFrame.background_label = Label(image=img, bg='#ffc917')
        self.inputStationFrame.background_label.img = img # keep a reference!
        self.inputStationFrame.background_label.place(x=550, y=520, relwidth=0.3, relheight=0.3)

class showInfoWindow():

    def __init__(self, parent, master):
        self.infoFrame = Frame(master=master, bg='#ffc917')
        self.infoFrame.pack(fill="none", expand=TRUE)
        self.infoLabel = Label(master=self.infoFrame, text='', bg='#ffc917')
        self.infoLabel.pack(ipadx=200, ipady=200)
        self.backbutton = Button(master=self.infoFrame, text='Terug', command=parent.viewInputStationFrame,
                                 height=3, width=10, bg='#0079d3', fg='white')
        self.backbutton.pack(padx=5, pady=10, expand=YES)


init()
