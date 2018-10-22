import requests
import xmltodict

def getStationInfo(stationName):
    auth_details = ('zico.gatsjadoerian@student.hu.nl', 'uOeCNT2uMzIIublGVSi6X2Gcpqg45U3IGmJy56C1lYuLilsl0HLfTQ')
    api_url = 'http://webservices.ns.nl/ns-api-avt?station=' + stationName

    response = requests.get(api_url, auth=auth_details)

    vertrekXML = xmltodict.parse(response.text)

    return vertrekXML


def data(stationName):
    dataXML = getStationInfo(stationName)
    data = ''
    for vertrek in dataXML['ActueleVertrekTijden']['VertrekkendeTrein'][:5]:
        eindbestemming = vertrek['EindBestemming']

        vertrektijd = vertrek['VertrekTijd']  # 2016-09-27T18:36:00+0200
        vertrektijd = vertrektijd[11:16]  # 18:36

        data += 'Om ' + vertrektijd + ' vertrekt een trein naar ' + eindbestemming + '\n'

    return data
