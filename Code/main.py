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

@app.route('/flat/all/getFlatTypes' , methods = ['GET'])
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

@app.route('/flat/all/getRegion' , methods = ['GET'])
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

@app.route('/flat/all/getFlatsByFilter' , methods = ['GET'])
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

@app.route('/flat/filter/getFlatRental' , methods = ['GET'])
def getFlatRental():
    input = request.args.get('fd_id')
    query_statement = "SELECT RT_ID,median_rent,RentalFlat.FD_ID,RentalFlat.QuarterID,year,quarter " \
                      "FROM (RentalFlat " \
                      "INNER JOIN Quarter ON RentalFlat.QuarterID = Quarter.QuarterID) " \
                      f"WHERE FD_ID = {input} " \
                      f"ORDER BY year,quarter ASC"
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

@app.route('/flat/filter/getFlatDetails' , methods = ['GET'])
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

@app.route('/flat/filter/getFlatPrice' , methods = ['GET'])
def getFlatPrice():
    input = request.args.get('fd_id')
    query_statement = "SELECT RS_ID,price,ResaleFlat.FD_ID,ResaleFlat.QuarterID,year,quarter " \
                      "FROM (ResaleFlat " \
                      "INNER JOIN Quarter ON ResaleFlat.QuarterID = Quarter.QuarterID) " \
                      f"WHERE FD_ID = {input} " \
                      f"ORDER BY year,quarter ASC;"
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

@app.route('/pmi/all/getPropertyType' , methods = ['GET'])
def getPropertyType():
    query_statement = "SELECT * FROM PropertyType"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)

    array = []
    for row in result:
        rowDict = {"FID": row[0], "room_type": row[1]}
        array.append(rowDict)

    output = {"Query": query_statement, "Results": array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}

@app.route('/pmi/all/getPMIByFilter' , methods = ['GET'])
def getPMIByFilter():
    pid_input = request.args.get('pid') #propertyTypeID
    proj_input = request.args.get('project') or ""
    street_input = request.args.get('street') or ""

    query_statement = "SELECT PMI_ID,project,street,typeOfArea,tenure,PMIDetails.PType_ID,propertyType "\
                      "FROM (PMIDetails " \
                      "INNER JOIN PropertyType ON PMIDetails.PType_ID = PropertyType.PType_ID) " \
                      f"WHERE project LIKE'%{proj_input}%' " \
                      f"AND street LIKE '%{street_input}%' "
    if pid_input:
        query_statement += f"AND PMIDetails.PType_ID = {pid_input};"
    else:
        query_statement += ";"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)
    array = []
    for row in result:
        rowDict ={"PMI_ID":row[0],"project":row[1],"street":row[2],"typeOfArea":row[3],"tenure":row[4],
                  "PType_ID":row[5], "propertyType":row[6]}
        array.append(rowDict)

    output = {"Query":query_statement,"Results":array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}

@app.route('/pmi/filter/getPMIRental' , methods = ['GET'])
def getPMIRental():
    pmi_id = request.args.get('pmi_id')
    query_statement = "SELECT PRENT_ID,areaRange,rent_price,PMI_ID,PMIRent.QuarterID,year,quarter " \
                      "FROM (PMIRent " \
                      "INNER JOIN Quarter ON PMIRent.QuarterID = Quarter.QuarterID) " \
                      f"WHERE PMI_ID = {pmi_id} " \
                      f"ORDER BY year,quarter ASC;"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)

    array = []
    for row in result:
        rowDict ={"PRENT_ID":row[0],"areaRange":row[1],"rent_price":row[2],"PMI_ID":row[3],"QuarterID":row[4],
                  "year":row[5],"quarter":row[6]}
        array.append(rowDict)

    output = {"Query":query_statement,"Results":array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}

@app.route('/pmi/filter/getPMISalesPrice' , methods = ['GET'])
def getPMISalesPrice():
    pmi_id = request.args.get('pmi_id')
    query_statement = "SELECT PSALE_ID,area,price,PMI_ID,PMISale.QuarterID,year,quarter " \
                      "FROM (PMISale " \
                      "INNER JOIN Quarter ON PMISale.QuarterID = Quarter.QuarterID) " \
                      f"WHERE PMI_ID = {pmi_id} " \
                      f"ORDER BY year,quarter ASC;"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)

    array = []
    for row in result:
        rowDict ={"PSALE_ID":row[0],"area":row[1],"price":row[2],"PMI_ID":row[3],"QuarterID":row[4],
                  "year":row[5],"quarter":row[6]}
        array.append(rowDict)

    output = {"Query":query_statement,"Results":array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}

@app.route('/view/addBookmark', methods = ['POST'])
def addBookmark():
    userID = request.form['UserID']
    pmi_id = request.form['PMI_ID'] or "NULL"
    fd_id = request.form['FD_ID'] or "NULL"
    description = request.form['description'] or ""
    query_statement = "INSERT INTO bookmark (description,userID,PMI_ID,FD_ID) " \
                      f"VALUES ('{description}',{userID},{pmi_id},{fd_id});"
    print(query_statement)
    cursor = conn.cursor()
    response = {}
    responseCode = 400
    try:
        cursor.execute(query_statement)
        conn.commit()
        response['success'] = 1
        responseCode = 200
    except:
        response['success'] = 0
        response['message'] = "Fail to insert"

    output = {"Query": query_statement, "Results": response}
    return json.dumps(output), responseCode, {'ContentType': 'application/json'}

@app.route('/view/getBookmark', methods = ['POST'])
def getBookmark():
    userID = request.form['UserID']
    query_statement = "SELECT BookmarkID,description,Bookmark.PMI_ID,Bookmark.FD_ID,lease_commence_date," \
                      "block,model,floor_area_sqm,RID,FID,project,street,typeOfArea,tenure,PType_ID " \
                      "FROM bookmark " \
                      "LEFT JOIN FlatDetails " \
                      "ON Bookmark.FD_ID = FlatDetails.FD_ID " \
                      "LEFT JOIN PMIDetails " \
                      "ON Bookmark.PMI_ID = PMIDetails.PMI_ID " \
                      f"WHERE UserID = {userID};"
    print(query_statement)

    cursor = conn.cursor()
    cursor.execute(query_statement)
    result = cursor.fetchall()
    print(result)

    array = []
    for row in result:
        rowDict = {"BookmarkID": row[0], "Description": row[1], "PMI_ID":row[2],"FD_ID": row[3],
                   "lease_commence_date": row[4],"block": row[5],"model":row[6],"floor_area_sqm":row[7],
                   "RID":row[8],"FID":row[9],"project":row[10],"street":row[11],"typeOfArea":row[12],
                    "tenure":row[13],"PType_ID":row[14]}
        array.append(rowDict)

    output = {"Query": query_statement, "Results": array}
    return json.dumps(output), 200, {'ContentType': 'application/json'}
