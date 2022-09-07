import requests
import json
import urllib
def convertPostalToAddress(postalcode):
    url = "https://geocode.search.hereapi.com/v1/geocode?apiKey=lXprRfCEPXvKtQpRl15-HfEbJx7yyeeRptzQMv8mWR0&q={}+SGP"
    url = url.format(postalcode)
    response = requests.get(url)
    print(response.json()["items"][0]["address"]["label"])



def privateResidentialPropertyTransactions():
    url = "https://data.gov.sg/api/action/datastore_search?resource_id=4541dd43-89a8-4e4b-881a-0cf1096489d0";
    response = requests.get(url)
    print(response.json())

privateResidentialPropertyTransactions()

# convertPostalToAddress(520843)
