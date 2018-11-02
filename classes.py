import sqlite3  # gebruik sqlite
import tkinter.messagebox  # import messagebox
from tkinter import *  # import alles van tkinter
import functions


class container():
    """

    Algemeen class dat alles van tkinter in zich neemt(wrapper)

    """

    def __init__(self, master):
        """

        De 2 scheremen die krijgen een eigen variable en kan je later aanroepen

        Args:
            master: Root van applicatie tkinter
        """
        self.inputStationWindow = inputStationWindow(self, master)  # Hoofdscherm met input field voor station
        self.showInfoWindow = showInfoWindow(self, master)  # 2de scherm, laat informatie zien van het station

    def viewInputStationFrame(self):
        """
            Functie die hoofdscherm laat zien
        """
        self.showInfoWindow.infoFrame.pack_forget()  # hide de informatie scherm
        self.inputStationWindow.inputStationFrame.pack(fill=NONE, expand=TRUE, ipadx=100,
                                                       ipady=100)  # laat het hoofdscherm zien
        self.inputStationWindow.inputField.delete(0, 'end')  # leeg de input field
        self.showInfoWindow.listbox.delete(0, 'end')  # clear de informatie van vorige station

    def viewInfoFrame(self):
        """
                    Functie die de informatiescherm laat zien
        """

        self.inputStationWindow.inputStationFrame.pack_forget()  # hide het hoofdscherm

        self.showInfoWindow.infoFrame.pack(fill=BOTH, expand=TRUE, pady=100, padx=100)  # laat de informatie scherm zien

    def showinfostation(self, currentStation=False):

        """

        Args:
            currentStation: Wordt er op huidige station geklikt dan is varaible station utrecht, anders False

        Returns:
            Return False als er geen match is, of station als er wel een match is
        """

        if currentStation:  # huidige station gklikt
            station = 'Utrecht'
        else:  # niet huidige station geklikt en gebruiker klikt op "vertrijktijden station"
            station = self.inputStationWindow.inputField.get()  # krijg informatie uit de input field
            if station == '':  # is het leeg laat error box zien
                tkinter.messagebox.showerror("Invoerveld leeg", "Gelieve iets in te voeren")  # error box
                return False  # stop met uitvoeren van deze functie

        db_conn = database()  # database verbinding class

        if station == 'update_station_list':  # wordt de commando ingetypt dan update station lijst
            db_conn.excel_to_db()  # lees excel bestand uit en stop het in de db
            tkinter.messagebox.showinfo("update", "Update compleet")  # message complete met uitvoeren

            return False  # stop met uitvoeren van deze functie

        valid_station = db_conn.read_from_db_by_input(station)  # kijk of station bekend is in db
        station_info = False

        if valid_station:  # is het een geldige station verkrijg informatie
            station_info = functions.data(valid_station)  # verkrijg informatie

        if station_info:  # is het niet False ga door
            self.showInfoWindow.infoLabel[
                "text"] = 'Huidig station: ' + valid_station + '\n'  # Huidige station naam ingevuld door gebruiker
            for station in station_info:  # loop informatie

                # station[0] = Tijd
                # station[1] = Vertraging
                # station[2] = Soort trein
                # station[3] = Naar locatie
                # station[4] = Spoor
                # station[5] = Route

                self.showInfoWindow.listbox.insert(END,
                                                   'Om {} {} vertrekt een {} naar {} op spoor: {}'.format(station[0],
                                                                                                          station[1],
                                                                                                          station[2],
                                                                                                          station[3],
                                                                                                          station[
                                                                                                              4]))  # insert informatie in scrollbare lijst

                if station[5]:  # is route meegelverd dan loop
                    for route in station[5].split(','):  # split string naar list bij komma en loop
                        self.showInfoWindow.listbox.insert(END, '   · {}'.format(route))

            self.viewInfoFrame()  # laat infoscherm zien

        elif station_info == 'conn_error':  # geen verbinding show error
            tkinter.messagebox.showerror("Error", 'Geen verbinding')  # messagebox geen verbinding
        else:  # station bestaat niet
            tkinter.messagebox.showerror("Error", 'Station bestaat niet!')  # messagebox geen station


class inputStationWindow():
    """
        Tkinter scherm voor hoofdscherm
    """

    def __init__(self, parent, master):
        """
            Functie roept getStationInfo aan en haalt de gegvens op bij de meegeleverde stationnaam

            Args:
                parent: Parent class container voor functies aanroepen
                master:  Tkinter master

        """

        self.inputStationFrame = Frame(master=master, bg='#ffc917', borderwidth=2, relief="groove")  # Frame aanmaken
        self.inputStationFrame.pack(fill="none", expand=TRUE)  # pack het
        self.title = Label(self.inputStationFrame, font=(20), text="Vul hier uw gewenste station in:", fg='white',
                           bg='#0079d3', height=3)  # label met text
        self.title.pack(pady=30)  # pack het
        self.inputField = Entry(master=self.inputStationFrame, font=(15))  # input field
        self.inputField.pack(pady=20, padx=10, ipady=10)  # plaats het
        self.inputButton = Button(master=self.inputStationFrame, text='Vertrektijden station',
                                  command=parent.showinfostation, height=3, bg='#0079d3', fg='white')  # knop
        self.inputButton.config(width='20')  # breedte knop
        self.inputButton.pack(padx=5, pady=0)  # plaats het

        self.currentButton = Button(master=self.inputStationFrame, text='     Huidig station     ',
                                    command=lambda: parent.showinfostation(True), height=3, bg='#0079d3',
                                    fg='white')  # knop
        self.currentButton.config(width='20')  # breedte knop

        self.currentButton.pack(padx=5, pady=10, side=LEFT, expand=YES)  # plaats het

        self.infButton = Button(master=self.inputStationFrame, command=self.infobutton, text='Info', height=3,
                                bg='#0079d3',
                                fg='white')  # knop
        self.infButton.config(width='20')  # breedte knop
        self.infButton.pack(padx=5, pady=10, side=LEFT, expand=YES)  # plaats het

        self.ovButton = Button(master=self.inputStationFrame, command=self.showbutton, text='Ov-chipkaart opladen',
                               height=3,
                               bg='#0079d3', fg='white')  # knop
        self.ovButton.config(width='20')  # breedte knop

        self.ovButton.pack(padx=5, pady=10, side=LEFT, expand=YES)  # plaats het
        img = PhotoImage(file='images/ns1.png')  # achtergrond plaatje
        self.inputStationFrame.background_label = Label(image=img, bg='#ffc917')  # achtergrond kleur
        self.inputStationFrame.background_label.img = img  # Set plaatje
        self.inputStationFrame.background_label.pack(side=BOTTOM)  # plaats het

    def showbutton(self):
        """
        Als knop gelikt wordt laat messagebox zien
        """
        tkinter.messagebox.showerror("Error", "Kaartverkoop is hier niet aanwezig")  # messagebox error

    def infobutton(self):
        """
            Als knop gelikt wordt laat messagebox zien
        """
        tkinter.messagebox.showinfo("Informatie",
                                    "Vertrektijden station: zodra u uw gewenste station succesvol invuld in het invoerveld kunt u op dit knop klikken. Zodra u er op klikt kunt u de 5 vertekkende treinen op het station zien. \n"
                                    "\nHuidig station: Zodra u hier op klikt zult u alle 5 vertrekkende treinen van dit station zien. \n" "\nOv-chipkaart opladen: Als u hier op klikt kunt u uw ov-chipkaart opladen.")  # informatie messagebox


class showInfoWindow():
    """
            Tkinter scherm voor informatiescherm
    """

    def __init__(self, parent, master):
        """
        Functie roept getStationInfo aan en haalt de gegvens op bij de meegeleverde stationnaam

        Args:
            parent: Parent class container voor functies aanroepen
            master:  Tkinter master

        """

        self.infoFrame = Frame(master=master, bg='#ffc917')  # frame scherm
        self.infoFrame.pack(fill="none", expand=TRUE)  # plaats het
        self.infoLabel = Label(master=self.infoFrame, text='', bg='#ffc917', font=(20),
                               relief="groove")  # text labeltje
        self.infoLabel.pack(ipadx=200, ipady=50)  # plaats het
        self.backbutton = Button(master=self.infoFrame, text='Terug', command=parent.viewInputStationFrame,
                                 height=3, width=10, bg='#0079d3', fg='white')  # terug knop
        self.backbutton.pack(padx=5, pady=10, expand=YES, side=TOP)  # plaats het
        self.scrollbar = Scrollbar(master=self.infoFrame)  # scrollbar om te scrollen
        self.scrollbar.pack(side=RIGHT, fill=BOTH)  # plaats het rechter kant
        self.listbox = Listbox(master=self.infoFrame, yscrollcommand=self.scrollbar.set,
                               height=30)  # scrolbare list en bind met scrollbar
        self.listbox.pack(side=TOP, fill=BOTH)  # plaats het


class database():
    """Exceptions are documented in the same way as classes.

    Algemeene database acties die benodigd zijn

    """

    def __init__(self):
        """
        Nieuwe instantie van database open de connectie
        """
        self.conn = sqlite3.connect('db/stations.db')  # connectie openen
        self.executer = self.conn.cursor()  # #hiermee kan je sql uitvoeren

    def execute(self, sql_command, parameter=False):
        """

        Args:
            sql_command: de sql command die uitgevoerd moet worden
            parameter: Als er paramters gebined moet worden voor de sql
        """
        if parameter:
            self.executer.execute(sql_command, [parameter])  # bind met paramter
        else:
            self.executer.execute(sql_command)  # voer de sql uit
        self.conn.commit()  # sla de execute op

    def disconnect(self):
        """
        Disconnect database
        """
        self.executer.close()  # sluit de executer
        self.conn.close()  # sluit de connectie

    def getSingleData(self, sql_command, parameter=False):
        """

        Args:
            sql_command: de sql command die uitgevoerd moet worden
            parameter: Als er paramters gebined moet worden voor de sql

        Returns:
            return data van database

        """


        if parameter:
            self.executer.execute(sql_command, [parameter])  # bind met paramter
        else:
            self.executer.execute(sql_command)  # voer de sql uit

        return self.executer.fetchone()  # return 1 resultaat

    def excel_to_db(self):
        """
        Leeg stations table en lees alles uit de csv bestand en stop dit in de database
        """
        self.execute("delete from stations")  # verwijder alles

        stations = functions.getStationInfo(None,True)

        for station in stations['stations']['station']:
            if 'NL' == station['country']:
                self.execute("INSERT INTO stations (name) VALUES (?)",station['name'])



        # with open('csv/stations.csv', 'r') as stationsFile:  # open het bestand en sluit wanneer klaar
        #     reader = csv.reader(stationsFile, delimiter=';')  # Lees bestand uit met splitser van ;
        #
        #     for station_name in reader:  # loop data
        #         self.execute("INSERT INTO stations (name) VALUES (?)",
        #                      station_name)  # stop het in de database en bind parameter

        self.disconnect()  # disconnect

    def read_from_db_by_input(self, input_station):
        """

        Args:
            input_station: Ingevoerde station van gebruiker

        Returns:
            Return False als er geen match is, of station als er wel een match is
        """
        if input_station == '%':
            input_station = ''

        data = self.getSingleData("SELECT * FROM stations WHERE name LIKE '%' || (?) || '%' LIMIT 1",input_station)  # verkrijg 1 station dat lijkt op de ingevoerde station
        self.disconnect()  # disconnect database

        match = False  # standaard geen overeenkomst

        if data is not None:
            match = data[0]  # wel een overeenkomst zet match naar overeenkomst

        return match  # verkrijg de volledige station naam

