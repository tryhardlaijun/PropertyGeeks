import requests
import json
import pandas as pd
import copy

# AccessKey = ""
AccessKey = input("Enter Access Key : ")

def createJsonCsvThroughUraApI(url,name): 
    #Set up header parameter
    myobj = {'AccessKey': AccessKey,
            'Token':getToken(),
            'User-Agent': 'Mozilla/5.0'}
    #Send post requrest
    resp = requests.post(url, headers=myobj)
    output = resp.json()["Result"]
    output = createRowsForNestedUsers( output,"rental")
    #Create result json file
    output.to_json("./csvFiles/" + name + ".json", orient='records', lines=True)

    #Create csv file
    convertListOfDictionaryToCSV(output,name)
    
    print("--------------------------------")
    print("Completed csv and json files creation")
    print("--------------------------------")
    # print(output)
    
    
def convertListOfDictionaryToCSV(listOfDictionary,name):
    #Using pandas to csv
    df = pd.DataFrame(listOfDictionary)
    df.to_csv("./csvFiles/" + name + ".csv" ,index=False)

def getToken():
    #Return daily token
    url="https://www.ura.gov.sg/uraDataService/insertNewToken.action"
    myobj = {'AccessKey': AccessKey, 'User-Agent': 'Mozilla/5.0'}
    token = requests.post(url, headers=myobj)
    return token.json()["Result"]

def createRowsForNestedUsers(nestedDict,field):
    nestedDict1 = []

    for x in nestedDict:
        for y in range(len(x[field])):
            d2 = copy.deepcopy(x)
            d2[field] = x[field][y]
            nestedDict1.append(d2)
    data = pd.json_normalize(nestedDict1)
    return data

# createJsonCsvThroughUraApI("https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=1","PMI_Resi_Transaction")
# createJsonCsvThroughUraApI("https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Rental_Median","PMI_Resi_Rental_Median")
createJsonCsvThroughUraApI("https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Rental&refPeriod=22q1","PMI_Resi_Rental&refPeriod=20q1")




# nestedDict = [{"location":"AMK", "home":[{"room":"1","door number":"3"},
#                                          {"room":"2","door number":"5"}]}, 
#             {"location":"Tamp", "home":[{"room":"2","door number":"5"},
#                                         {"room":"3","door number":"8"}]}
#               ]
# nestedDict1 = []

# for x in nestedDict:
#     for y in range(len(x["home"])):
#         d2 = copy.deepcopy(x)
#         d2["home"] = x["home"][y]
#         nestedDict1.append(d2)
# data = pd.json_normalize(nestedDict1)
# data = pd.DataFrame(data)
# print(data)
# # print(a)