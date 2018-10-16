import urllib
import requests
import xmltodict

api_url = 'http://webservices.ns.nl/'
auth_details = ('', '')

def request(method, arguments):
    parameters = urllib.parse.urlencode(arguments)
    request_url = api_url + 'ns-api-' + method + '?' + parameters

    response = requests.get(request_url, auth=auth_details)
    xml = xmltodict.parse(response.text)

    return xml

def requestActualDepartureTimes(station):
    return request('avt', {'station': station})canv