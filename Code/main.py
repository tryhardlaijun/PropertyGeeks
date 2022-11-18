import mysql.connector
from flask import Flask, request
import json

app = Flask(__name__)

conn = mysql.connector.connect(user='normanchia', password='normanchia',
                              host='localhost',database='ict2102')
if conn:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")

@app.route('/')
def default():
    return "Hello World"

@app.route('/all/getFlatTypes' , methods = ['GET'])
def getFlatTypes():
    query_statement = "SELECT * FROM FlatType"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)

    array = []
    for row in result:
        rowDict ={"FID":row[0],"room_type":row[1]}
        array.append(rowDict)

    output = {"Query": query_statement, "Results": array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}

@app.route('/all/getQuarter' , methods = ['GET'])
def getQuarter():
    query_statement = "SELECT * FROM Quarter"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)
    array=[]
    for row in result:
        rowDict ={"QuarterID":row[0],"year":row[1],"quarter":row[2]}
        array.append(rowDict)

    output = {"Query":query_statement,"Results":array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}

@app.route('/all/getRegion' , methods = ['GET'])
def getRegion():
    query_statement = "SELECT * FROM Region"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)

    array = []
    for row in result:
        rowDict ={"RID":row[0],"town":row[1]}
        array.append(rowDict)

    output = {"Query": query_statement, "Results": array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}

@app.route('/all/getFlatsByFilter' , methods = ['GET'])
def getFlatByFilter():
    fid_input = request.args.get('fid')
    rid_input = request.args.get('rid')
    query_statement = "SELECT FD_ID, lease_commence_date, block, model,floor_area_sqm, town, room_type, " \
                      "FlatDetails.RID, FlatDetails.FID  " \
                      "FROM ((FlatDetails INNER JOIN Region ON FlatDetails.RID = Region.RID) " \
                      "INNER JOIN FlatType ON FlatDetails.FID = FlatType.FID) "
    if fid_input and rid_input:
        query_statement += f"WHERE FlatDetails.FID = {fid_input} AND FlatDetails.RID = {rid_input};"
    elif fid_input:
        query_statement += f"WHERE FlatDetails.FID = {fid_input};"
    elif rid_input:
        query_statement += f"WHERE FlatDetails.RID = {rid_input};"
    else:
        query_statement += ";"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)
    array = []
    for row in result:
        rowDict ={"FD_ID":row[0],"lease_commence_date":row[1],"block":row[2],"model":row[3],"floor_area_sqm":row[4],
                  "town":row[5],"room_type":row[6],"RID":row[7],"FID":row[8]}
        array.append(rowDict)

    output = {"Query":query_statement,"Results":array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}

@app.route('/filter/getFlatRental' , methods = ['GET'])
def getFlatRental():
    input = request.args.get('fd_id')
    query_statement = "SELECT RT_ID,median_rent,RentalFlat.FD_ID,RentalFlat.QuarterID,year,quarter " \
                      "FROM (RentalFlat " \
                      "INNER JOIN Quarter ON RentalFlat.QuarterID = Quarter.QuarterID) " \
                      f"WHERE FD_ID = {input};"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)

    array = []
    for row in result:
        rowDict ={"RT_ID":row[0],"median_rent":row[1],"QuarterID":row[3],"year":row[4],"quarter":row[5]}
        array.append(rowDict)

    output = {"Query":query_statement,"Results":array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}

@app.route('/filter/getFlatDetails' , methods = ['GET'])
def getFlatDetails():
    input = request.args.get('fd_id')

    query_statement = "SELECT FD_ID, lease_commence_date, block, model,floor_area_sqm, town, room_type, " \
                      "FlatDetails.RID, FlatDetails.FID " \
                      "FROM ((FlatDetails " \
                      "INNER JOIN Region ON FlatDetails.RID = Region.RID) " \
                      "INNER JOIN FlatType ON FlatDetails.FID = FlatType.FID) " \
                      f"WHERE FD_ID = {input};"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)
    row = result[0]
    array ={"FD_ID":row[0],"lease_commence_date":row[1],"block":row[2],"model":row[3],"floor_area_sqm":row[4],
            "town":row[5],"room_type":row[6],"RID":row[7],"FID":row[8]}

    output = {"Query":query_statement,"Results":array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}

@app.route('/filter/getFlatPrice' , methods = ['GET'])
def getFlatPrice():
    input = request.args.get('fd_id')
    query_statement = "SELECT RS_ID,price,ResaleFlat.FD_ID,ResaleFlat.QuarterID,year,quarter " \
                      "FROM (ResaleFlat " \
                      "INNER JOIN Quarter ON ResaleFlat.QuarterID = Quarter.QuarterID) " \
                      f"WHERE FD_ID = {input};"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)

    array = []
    for row in result:
        rowDict ={"RS_ID":row[0],"price":row[1],"QuarterID":row[3],"year":row[4],"quarter":row[5]}
        array.append(rowDict)

    output = {"Query":query_statement,"Results":array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}

