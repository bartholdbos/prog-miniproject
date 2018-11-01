import requests
import xmltodict
from tkinter import messagebox
import csv
import sqlite3

def getStationInfo(stationName):


    if not stationName:
        return False


    auth_details = ('zico.gatsjadoerian@student.hu.nl', 'uOeCNT2uMzIIublGVSi6X2Gcpqg45U3IGmJy56C1lYuLilsl0HLfTQ')
    api_url = 'http://webservices.ns.nl/ns-api-avt?station=' + stationName

    try:
        response = requests.get(api_url, auth=auth_details)
    except requests.ConnectionError:
        return 'conn_error'


    vertrekXML = xmltodict.parse(response.text)

    if 'error' in vertrekXML:
        messagebox.showerror("Error", vertrekXML['error']['message'])


    return vertrekXML


def data(stationName):
    dataXML = getStationInfo(stationName)
    data = []


    if dataXML == False:
        return False

    if 'error' not in dataXML:
        for vertrek in dataXML['ActueleVertrekTijden']['VertrekkendeTrein']:
            eindbestemming = vertrek['EindBestemming']
            vertrektijd = vertrek['VertrekTijd']  # 2016-09-27T18:36:00+0200
            vertrektijd = vertrektijd[11:16]  # 18:36


            try:
                spoor = vertrek['VertrekSpoor']['#text']
            except KeyError:
                spoor = 'Spoor niet beschikbaar'

            try:
                trein_soort = vertrek['TreinSoort']
            except KeyError:
                trein_soort = 'trein'

            try:
                vertraging = 'vertraging' + vertrek['VertrekVertragingTekst']
            except KeyError:
                vertraging = ''

            try:
                route = vertrek['RouteTekst']
            except KeyError:
                route = ''


            data += [[vertrektijd,vertraging,trein_soort,eindbestemming,spoor,route]]


    return data







class database():

    def __init__(self):
        self.conn = sqlite3.connect('stations.db')
        self.executer = self.conn.cursor()

    def execute(self,sql_command,parameter = False):
        if parameter:
            self.executer.execute(sql_command,parameter)
        else:
            self.executer.execute(sql_command)
        self.conn.commit()

    def disconnect(self):
        self.executer.close()
        self.conn.close()

    def getSingleData(self,sql_command):
        self.executer.execute(sql_command)
        return self.executer.fetchone()



    def create_table(self):

        self.execute("CREATE TABLE IF NOT EXISTS stations( name TEXT)")
        self.disconnect()

    def excel_to_db(self):

        self.execute("delete from stations")

        with open('stations.csv', 'r') as stationsFile:
            reader = csv.reader(stationsFile, delimiter=';')

            for station_name in reader:
                self.execute("INSERT INTO stations (name) VALUES (?)",station_name)

        self.disconnect()


    def read_from_db_by_input(self,input_station):
        data = self.getSingleData('SELECT * FROM stations WHERE name LIKE "%' + input_station + '%" LIMIT 1')
        self.disconnect()

        match = False

        if data is not None:
            match = data[0]

        return match



