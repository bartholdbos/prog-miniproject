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
        self.inputStationWindow.inputStationFrame.pack(fill="none", expand=TRUE, ipadx=100, ipady=100)

    def viewInfoFrame(self):

        self.inputStationWindow.inputStationFrame.pack_forget()
        self.showInfoWindow.infoFrame.pack(fill="none", expand=TRUE, ipadx=100, ipady=100)

    def showinfostation(self, currentStation = False):
        if currentStation:
            station = 'Utrecht'
        else:
            station = self.inputStationWindow.inputField.get()
            if station == '':
                messagebox.showerror("Invoerveld leeg", "Gelieve iets in te voeren")
        print(data(station))
        self.showInfoWindow.infoLabel["text"] = 'Huidig station: '+station + '\n'
        self.showInfoWindow.infoLabel["text"] += data(station)

        self.viewInfoFrame()
def showbutton():
    messagebox.showerror("Error", "Kaartverkoop is hier niet aanwezig")

def infobutton():
    messagebox.showerror("Informatie", "vertrektijden station: zodra u uw gewenste station succesvol invuld in het invoerveld kunt u op dit knop klikken. Zodra u er op klikt kunt u de 5 vertekkende treinen op het station zien. \n"
                                       "\nHuidig station: Zodra u hier op klikt zult u alle 5 vertrekkende treinen van dit station zien. \n" "\nOv-chipkaart opladen: Als u hier op klikt kunt u uw ov-chipkaart opladen.")


class inputStationWindow():

    def __init__(self, parent, master):
        self.inputStationFrame = Frame(master=master, bg='#ffc917', borderwidth=2, relief="groove")
        self.inputStationFrame.grid_propagate(False)
        self.inputStationFrame.pack(fill="none", expand=TRUE)
        self.title = Label(self.inputStationFrame, font=(20), text="Vul hier uw gewenste station in:", fg='white', bg='#0079d3', height=3)
        self.title.pack(pady=30)
        self.inputField = Entry(master=self.inputStationFrame,font=(15))
        self.inputField.pack(pady=20, padx=10, ipady=10)
        self.inputButton = Button(master=self.inputStationFrame, text='vertrektijden station',
                                  command=parent.showinfostation, height=3, bg='#0079d3', fg='white')
        self.inputButton.pack(padx=5, pady=0)

        self.currentButton = Button(master=self.inputStationFrame, text='     Huidig station     ',
                                  command=lambda : parent.showinfostation(True), height=3, bg='#0079d3', fg='white')
        self.currentButton.pack(padx=5, pady=10, side=LEFT, expand=YES)

        self.infButton = Button(master=self.inputStationFrame, command=infobutton, text='             Info              ', height=3, bg='#0079d3', fg='white')
        self.infButton.pack(padx=5, pady=10, side=LEFT, expand=YES)

        self.ovButton = Button(master=self.inputStationFrame, command=showbutton, text='Ov-chipkaart opladen', height=3, bg='#0079d3', fg='white')
        self.ovButton.pack(padx=5, pady=10, side=LEFT, expand=YES)
        img = PhotoImage(file='ns1.png')
        self.inputStationFrame.background_label = Label(image=img, bg='#ffc917')
        self.inputStationFrame.background_label.img = img # keep a reference!
        self.inputStationFrame.background_label.pack(side=BOTTOM)

class showInfoWindow():

    def __init__(self, parent, master):
        self.infoFrame = Frame(master=master, bg='#ffc917')
        self.infoFrame.pack(fill="none", expand=TRUE)
        self.infoLabel = Label(master=self.infoFrame, text='', bg='#ffc917', font=(20), borderwidth=2, relief="groove")
        self.infoLabel.pack(ipadx=200, ipady=50)
        self.backbutton = Button(master=self.infoFrame, text='Terug', command=parent.viewInputStationFrame,
                                 height=3, width=10, bg='#0079d3', fg='white')
        self.backbutton.pack(padx=5, pady=10, expand=YES, side=TOP)


init()
