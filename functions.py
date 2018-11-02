import requests  # request voor api
import xmltodict  # xml naar dictonary
import tkinter.messagebox  # import messagebox
from tkinter import *  # import alles van tkinter
import classes


def init():
    """
        Init het scherm met de functies
    """
    root = Tk()

    root.state('zoomed')
    root.configure(bg='#ffc917')
    mainContainer = classes.container(root)
    mainContainer.viewInputStationFrame()

    root.mainloop()

def getStationInfo(stationName,station_list = False):
    """

    Haal gegevens op van station met de meegegevende stationsnaam

    Args:
        stationName: Station naam om gegevens op te halen
        station_list: true dan verkrijg station lijst

    Returns:
        return xml van api .
    """

    auth_details = ('zico.gatsjadoerian@student.hu.nl',
                    'uOeCNT2uMzIIublGVSi6X2Gcpqg45U3IGmJy56C1lYuLilsl0HLfTQ')  # auth gegevens op teogang te krijgen

    if station_list:
        api_url = 'http://webservices.ns.nl/ns-api-stations' # alle station namen
    else:
        api_url = 'http://webservices.ns.nl/ns-api-avt?station=' + stationName  # url waar de api kan verbinden


    try:  # als er geen connectie fout is krijg de response
        response = requests.get(api_url, auth=auth_details)  # krijg response
    except requests.ConnectionError:  # asl er wel een connectie fout is
        return 'conn_error'  # geen verbinding

    vertrekXML = xmltodict.parse(response.text)  # response naar xml parsen

    if 'error' in vertrekXML:  # zit er error in de response display een foutmelding
        tkinter.messagebox.showerror("Error", vertrekXML['error']['message'])

    return vertrekXML  # return xml van api


def data(stationName):
    """
    Functie roept getStationInfo aan en haalt de gegvens op bij de meegeleverde stationnaam

    Args:
        stationName: Station naam

    Returns:
        return data in een nested list .

    """
    dataXML = getStationInfo(stationName)  # roep functie getStationInfo aan om gegevens van de api op te halen
    data = []  # set data leeg

    if dataXML == False:
        return False  # als stationnaam niet bestaat return False

    if 'error' not in dataXML:
        for vertrek in dataXML['ActueleVertrekTijden']['VertrekkendeTrein']:
            eindbestemming = vertrek['EindBestemming']
            vertrektijd = vertrek['VertrekTijd']  # 2016-09-27T18:36:00+0200
            vertrektijd = vertrektijd[11:16]  # 18:36

            try:  # spoorlijn, als er een bijv een bus is krijgt het "Spoor niet beschikbaar"
                spoor = vertrek['VertrekSpoor']['#text']
            except KeyError:
                spoor = 'Spoor niet beschikbaar'

            try:  # Treinsoort bekend krijgt het de treinsoort anders standaard trein
                trein_soort = vertrek['TreinSoort']
            except KeyError:
                trein_soort = 'trein'

            try:  # is er vetraging zoja laat de vertraging zien anders niks
                vertraging = 'vertraging' + vertrek['VertrekVertragingTekst']
            except KeyError:
                vertraging = ''

            try:  # is er een routetekst laat de routetekst zien anders niks
                route = vertrek['RouteTekst']
            except KeyError:
                route = ''

            # station[0] = Tijd
            # station[1] = Vertraging
            # station[2] = Soort trein
            # station[3] = Naar locatie
            # station[4] = Spoor
            # station[5] = route
            data += [[vertrektijd, vertraging, trein_soort, eindbestemming, spoor, route]]  # voeg toe aan list

    return data  # return data nested list





