import sqlite3 # gebruik sqlite
import csv # gebruik csv leesbaarheid

class database():

    """Exceptions are documented in the same way as classes.

    Algemeene database acties die benodigd zijn

    """

    def __init__(self):
        """
        Nieuwe instantie van database open de connectie
        """
        self.conn = sqlite3.connect('db/stations.db') # connectie openen
        self.executer = self.conn.cursor()  # #hiermee kan je sql uitvoeren

    def execute(self, sql_command, parameter=False):
        """

        Args:
            sql_command: de sql command die uitgevoerd moet worden
            parameter: Als er paramters gebined moet worden voor de sql
        """
        if parameter:
            self.executer.execute(sql_command, parameter) # bind met paramter
        else:
            self.executer.execute(sql_command) # voer de sql uit
        self.conn.commit() # sla de execute op

    def disconnect(self):
        """
        Disconnect database
        """
        self.executer.close() # sluit de executer
        self.conn.close() # sluit de connectie

    def getSingleData(self, sql_command):
        """

        Args:
            sql_command: de sql command die uitgevoerd moet worden

        Returns:
            return data van database

        """
        self.executer.execute(sql_command) # voer uit
        return self.executer.fetchone() # return 1 resultaat

    def excel_to_db(self):
        """
        Leeg stations table en lees alles uit de csv bestand en stop dit in de database
        """
        self.execute("delete from stations") #verwijder alles

        with open('csv/stations.csv', 'r') as stationsFile: # open het bestand en sluit wanneer klaar
            reader = csv.reader(stationsFile, delimiter=';') # Lees bestand uit met splitser van ;

            for station_name in reader: # loop data
                self.execute("INSERT INTO stations (name) VALUES (?)", station_name) # stop het in de database en bind parameter

        self.disconnect() # disconnect

    def read_from_db_by_input(self, input_station):
        """

        Args:
            input_station: Ingevoerde station van gebruiker

        Returns:
            Return False als er geen match is, of station als er wel een match is
        """
        data = self.getSingleData('SELECT * FROM stations WHERE name LIKE "%' + input_station + '%" LIMIT 1') # verkrijg 1 station dat lijkt op de ingevoerde station
        self.disconnect() # disconnect database

        match = False # standaard geen overeenkomst

        if data is not None:
            match = data[0] # wel een overeenkomst zet match naar overeenkomst

        return match #verkrijg de volledige station naam