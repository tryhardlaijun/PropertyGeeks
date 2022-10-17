import requests
import json
import urllib
import pandas as pd

dataGov = {
    "Median Rent by Town and Flat Type" : "6b1ec2ff-7c38-4ce9-9bbb-af865b4d78cb",
    "Resale Flat Prices": "f1765b54-a209-4718-8d38-a39237f502b3",
    "HDB Property Information" : "482bfa14-2977-4035-9c61-c85f871daf4e"
}

def dataGovToJson(resourceID,name):
    url = "https://data.gov.sg/api/action/datastore_search?&limit=10000&resource_id={}";
    response = requests.get(url.format(resourceID))
    # print((response.json()['result']['records']))
    df = pd.DataFrame(response.json()['result']['records'])
    df.to_csv("./csvFiles/" + name + ".csv" ,index=False)
    
# def convertListOfDictionaryToCSV(listOfDictionary,name):
#     df.to_csv("./csvFiles/" + name + ".csv" ,index=False)
dataGovToJson(dataGov["Median Rent by Town and Flat Type"],"dataGovMedianRentByTownAndFlat")
dataGovToJson(dataGov["Resale Flat Prices"],"dataGovResaleFlatPrices")
dataGovToJson(dataGov["HDB Property Information"],"dataGovHDBPropertyInformation")