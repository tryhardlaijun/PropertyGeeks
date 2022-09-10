import requests
import json
import urllib
import pandas as pd
def convertPostalToAddress(postalcode,api):
    url = "https://geocode.search.hereapi.com/v1/geocode?apiKey=" +api+ "&q={}+SGP"
    url = url.format(postalcode)
    response = requests.get(url)
    print(response.json()["items"][0]["address"]["label"])

convertPostalToAddress("850244", input("Please enter your API key : "))