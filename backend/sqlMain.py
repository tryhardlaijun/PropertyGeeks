import mysql.connector
from flask import Flask, request
import json

app = Flask(__name__)
limit = 10000
try:
    conn = mysql.connector.connect(user='normanchia', password='normanchia',
                              host='localhost',database='ict2102')
    print(conn)
    print("Connection Successful")
except:
    print("Connection Not Established")

@app.route('/')
def default():
    return "Hello World"

@app.route('/all/getQuarter' , methods = ['GET'])
def getQuarter():
    response_code = 400
    output = {}
    try:
        if conn:
            query_statement = "SELECT * FROM Quarter"
            print(query_statement)
            cursor = conn.cursor()
            cursor.execute(query_statement)
            result = cursor.fetchall()
            print(result)
            array = []
            for row in result:
                rowDict = {"QuarterID": row[0], "year": row[1], "quarter": row[2]}
                array.append(rowDict)
            output = {"Query": query_statement, "Count": len(array), "Results": array}
            response_code = 200
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output),response_code,{'ContentType': 'application/json'}

@app.route('/flat/all/getFlatTypes' , methods = ['GET'])
def getFlatTypes():
    response_code = 400
    output = {}
    try:
        if conn:
            query_statement = "SELECT * FROM FlatType"
            cursor = conn.cursor()
            cursor.execute(query_statement)
            result = cursor.fetchall()
            print(result)
            array = []
            for row in result:
                rowDict ={"FID":row[0],"room_type":row[1]}
                array.append(rowDict)
            output = {"Query": query_statement, "Count": len(array), "Results": array}
            response_code = 200
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output),response_code,{'ContentType': 'application/json'}

@app.route('/flat/all/getRegion' , methods = ['GET'])
def getRegion():
    response_code = 400
    output = {}
    try:
        if conn:
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
            output = {"Query":query_statement,"Count":len(array),"Results":array}
            response_code = 200
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}

@app.route('/flat/all/getFlatsByFilter' , methods = ['GET'])
def getFlatByFilter():
    response_code = 400
    output = {}
    try:
        if conn:
            fid_input = request.args.get('fid')
            rid_input = request.args.get('rid')
            query_statement = "SELECT FD_ID, lease_commence_date, block, model,floor_area_sqm, town, room_type, " \
                              "FlatDetails.RID, FlatDetails.FID  " \
                              "FROM ((FlatDetails INNER JOIN Region ON FlatDetails.RID = Region.RID) " \
                              "INNER JOIN FlatType ON FlatDetails.FID = FlatType.FID) "
            if fid_input and rid_input:
                query_statement += f"WHERE FlatDetails.FID = {fid_input} AND FlatDetails.RID = {rid_input} "
            elif fid_input:
                query_statement += f"WHERE FlatDetails.FID = {fid_input} "
            elif rid_input:
                query_statement += f"WHERE FlatDetails.RID = {rid_input} "
            query_statement += f"LIMIT {limit};"
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
            output = {"Query":query_statement,"Count":len(array),"Results":array}
            response_code = 200
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}

@app.route('/flat/filter/getFlatRental' , methods = ['GET'])
def getFlatRental():
    response_code = 400
    output = {}
    try:
        if conn:
            input = request.args.get('fd_id')
            if input is None:
                raise Exception("fd_id parameter is empty.")
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
            output = {"Query":query_statement,"Count":len(array),"Results":array}
            response_code = 200
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}

@app.route('/flat/filter/getFlatDetails' , methods = ['GET'])
def getFlatDetails():
    response_code = 400
    output = {}
    try:
        if conn:
            input = request.args.get('fd_id')
            if input is None:
                raise Exception("fd_id parameter is empty.")
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
            output = {"Query":query_statement,"Count":len(array),"Results":array}
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}

@app.route('/flat/filter/getFlatPrice' , methods = ['GET'])
def getFlatPrice():
    response_code = 400
    output = {}
    try:
        if conn:
            input = request.args.get('fd_id')
            if input is None:
                raise Exception("fd_id parameter is empty.")
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
            output = {"Query":query_statement,"Count":len(array),"Results":array}
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}

@app.route('/pmi/all/getPropertyType' , methods = ['GET'])
def getPropertyType():
    response_code = 400
    output = {}
    try:
        if conn:
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
            output = {"Query":query_statement,"Count":len(array),"Results":array}
            response_code = 200
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}

@app.route('/pmi/all/getPMIByFilter' , methods = ['GET'])
def getPMIByFilter():
    response_code = 400
    output = {}
    try:
        if conn:
            pid_input = request.args.get('pid') #propertyTypeID
            proj_input = request.args.get('project') or ""
            street_input = request.args.get('street') or ""
            query_statement = "SELECT PMI_ID,project,street,typeOfArea,tenure,PMIDetails.PType_ID,propertyType "\
                              "FROM (PMIDetails " \
                              "INNER JOIN PropertyType ON PMIDetails.PType_ID = PropertyType.PType_ID) " \
                              f"WHERE project LIKE'%{proj_input}%' " \
                              f"AND street LIKE '%{street_input}%' "
            if pid_input:
                query_statement += f"AND PMIDetails.PType_ID = {pid_input} "
            query_statement += f"LIMIT {limit};"
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
            output = {"Query":query_statement,"Count":len(array),"Results":array}
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}

@app.route('/pmi/filter/getPMIRental' , methods = ['GET'])
def getPMIRental():
    response_code = 400
    output = {}
    try:
        if conn:
            input = request.args.get('pmi_id')
            if input is None:
                raise Exception("pmi_id parameter is empty.")
            query_statement = "SELECT PRENT_ID,areaRange,rent_price,PMI_ID,PMIRent.QuarterID,year,quarter " \
                              "FROM (PMIRent " \
                              "INNER JOIN Quarter ON PMIRent.QuarterID = Quarter.QuarterID) " \
                              f"WHERE PMI_ID = {input} " \
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
            output = {"Query":query_statement,"Count":len(array),"Results":array}
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}

@app.route('/pmi/filter/getPMISalesPrice' , methods = ['GET'])
def getPMISalesPrice():
    response_code = 400
    output = {}
    try:
        if conn:
            input = request.args.get('pmi_id')
            if input is None:
                raise Exception("pmi_id parameter is empty.")
            query_statement = "SELECT PSALE_ID,area,price,PMI_ID,PMISale.QuarterID,year,quarter " \
                              "FROM (PMISale " \
                              "INNER JOIN Quarter ON PMISale.QuarterID = Quarter.QuarterID) " \
                              f"WHERE PMI_ID = {input} " \
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
            output = {"Query":query_statement,"Count":len(array),"Results":array}
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}

@app.route('/view/addBookmark', methods = ['POST'])
def addBookmark():
    output = {}
    response_code = 400
    try:
        if conn:
            user_id = request.form.get('UserID')
            pmi_id = request.form.get('PMI_ID') or "NULL"
            fd_id = request.form.get('FD_ID') or "NULL"
            description = request.form.get('description') or ""
            if user_id is None:
                raise Exception("User ID parameter is empty.")
            if pmi_id == "NULL" and fd_id == "NULL":
                raise Exception("PMI and FD ID parameter is empty. Need 1 field to be filled")
            query_statement = "INSERT INTO bookmark (description,userID,PMI_ID,FD_ID) " \
                              f"VALUES ('{description}',{user_id},{pmi_id},{fd_id});"
            print(query_statement)
            cursor = conn.cursor()
            cursor.execute(query_statement)
            conn.commit()
            output['success'] = 1
            response_code = 200
            output = {"Query": query_statement, "Results": output}
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}

@app.route('/view/getBookmark', methods = ['POST'])
def getBookmark():
    response_code = 400
    output = {}
    try:
        if conn:
            input = request.form.get('UserID')
            if input is None:
                raise Exception("User ID parameter is empty.")
            query_statement = "SELECT BookmarkID,description,Bookmark.PMI_ID,Bookmark.FD_ID,lease_commence_date," \
                              "block,model,floor_area_sqm,RID,FID,project,street,typeOfArea,tenure,PType_ID " \
                              "FROM bookmark " \
                              "LEFT JOIN FlatDetails " \
                              "ON Bookmark.FD_ID = FlatDetails.FD_ID " \
                              "LEFT JOIN PMIDetails " \
                              "ON Bookmark.PMI_ID = PMIDetails.PMI_ID " \
                              f"WHERE UserID = {input};"
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
            output = {"Query":query_statement,"Count":len(array),"Results":array}
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}


@app.route('/view/deleteBookmark', methods = ['POST'])
def deleteBookmark():
    response_code = 400
    output = {}
    try:
        if conn:
            user_id = request.form.get('UserID')
            bookmark_id = request.form.get('bookmark_id')
            if user_id is None:
                raise Exception("User ID parameter is empty.")
            if bookmark_id is None:
                raise Exception("Bookmark ID parameter is empty.")
            query_statement = "DELETE FROM Bookmark " \
                              f"WHERE UserID = {user_id} " \
                              f"AND BookmarkID = {bookmark_id};"
            print(query_statement)
            cursor = conn.cursor()
            cursor.execute(query_statement)
            conn.commit()
            output['success'] = 1
            response_code = 200
            output = {"Query": query_statement, "Results": output}
    except Exception as e:
        response_code = 400
        output = {"result": 0, "message": "Unable to connect to database", "error": str(e)}
    finally:
        return json.dumps(output), response_code, {'ContentType': 'application/json'}
