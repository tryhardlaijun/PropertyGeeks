from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from datetime import datetime
import pymongo
import json
import sys
from bson.json_util import dumps, loads

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://Cluster73324:qpwoeiruty@cluster73324.dsnxfd1.mongodb.net/?retryWrites=true&w=majority")
try:
    client.server_info()
except pymongo.errors.OperationFailure as err:
    print ("Connection Not Established. Exit the system")
    sys.exit(0) 

print ("Connected Successfully")
db = client['2103_database']
col = db["PropertyGeeks"]

# with open('ResaleHDB_nosql.json') as file:
#     file_data = json.load(file)
# col.insert_many(file_data)

@app.route('/' , methods = ["GET"])
def default():
    return "WELCOME TO PROPERTY GEEKS"

@app.route('/flat/all/getFlatTypes', methods= ['GET'])
def getFlatTypes():
    col = db["PropertyGeeks"]
    queryStatement = col.aggregate([{"$group": {
            "_id": "$room_type"}}])
    return list(queryStatement) 

@app.route('/flat/all/getQuarter' , methods = ['GET'])
def getQuarter():
    col = db["PropertyGeeks"]
    queryStatement = col.aggregate([
        {"$match":{
            "RT_ID":{
                "$exists": "true"
            },
        }},
        {"$group": {
            "_id": {
                "year":"$year",
                "quarter": "$quarter"
        }}},
        { "$sort":{"_id.year":1,"_id.quarter":1}},
        ])
    return list(queryStatement)

@app.route('/flat/all/getRegion' , methods = ['GET'])
def getRegion():
    col = db["PropertyGeeks"]
    # col2 = db["RentPMI"]
    queryStatement = col.aggregate([
        {"$group": {
            "_id": "$town"}},
        { "$sort":{"_id.year":1,"_id.quarter":1}}
        ])
    return list(queryStatement)

@app.route('/flat/all/getFlatsByFilter' , methods = ['GET'])
def getFlatByFilter():
    col = db["PropertyGeeks"]
    flat_type = request.args.get("flat_type")
    Region = request.args.get("Region")
    pipeline = [
    {
        "$match":{
            "$or":[
            {
                "RT_ID":{
                    "$exists": "true"
            }},
            {
                "RS_ID":{
                    "$exists": "true"
            }}
            ],
        }},
        ]
    if flat_type and Region:
        pipeline[0]["$match"]["town"] = Region
        pipeline[0]["$match"]["room_type"] = flat_type
        print("HELLO")
        
    elif flat_type and not Region:
        pipeline[0]["$match"]["room_type"] = flat_type
    elif not flat_type and Region:
        pipeline[0]["$match"]["town"] = Region
    pipeline.append({
            "$project":{    
                "_id":0,
                "median_rent": 0,
            }
        })
    queryStatement = col.aggregate(pipeline)
    return dumps(list(queryStatement),indent=4), 200, {'ContentType': 'application/json'}

@app.route('/flat/filter/getFlatRental' , methods = ['GET'])
def getFlatRental():
    rentID = request.args.get("rentID")
    pipeline = [
    {
        "$match":{
            "RT_ID":{
                "$exists": "true"
            },
            "RT_ID": rentID
        }
    },
    {
        "$project":{    
            "_id":0,
            "town":0,
            "floor_area_sqm":0,
            "lease_commence_date": 0,
            "block": 0,
            "model": 0,
            # "median_rent": 0,
        }
    }
    ]
    queryStatement = col.aggregate(pipeline)
    return dumps(list(queryStatement),indent=4), 200, {'ContentType': 'application/json'}


@app.route('/flat/filter/getRentFlatDetails' , methods = ['GET'])
def getRentFlatDetails():
    rentID = request.args.get("rentID")
    pipeline = [
    {
         "$match":{
            "RT_ID":{
                "$exists": "true"
            },
            "RT_ID": rentID
        }
    },
    {
        "$project":{    
            "_id":0,
        }
    }
    ]
    queryStatement = col.aggregate(pipeline)
    return dumps(list(queryStatement),indent=4), 200, {'ContentType': 'application/json'}

@app.route('/flat/filter/getResaleFlatDetails' , methods = ['GET'])
def getResaleFlatDetails():
    resaleID = request.args.get("resaleID")
    pipeline = [
    {
         "$match":{
            
                "RS_ID":{
                    "$exists": "true"
            },
            "RS_ID": int(resaleID)
        }
    },
    {
        "$project":{    
            "_id":0,
        }
    }
    ]
    queryStatement = col.aggregate(pipeline)
    return dumps(list(queryStatement),indent=4), 200, {'ContentType': 'application/json'}

@app.route('/flat/filter/getFlatPrice' , methods = ['GET'])
def getFlatPrice():
    resaleID = request.args.get("resaleID")
    query_statement = "SELECT RS_ID,price,ResaleFlat.FD_ID,ResaleFlat.QuarterID,year,quarter " \
                      "FROM (ResaleFlat " \
                      "INNER JOIN Quarter ON ResaleFlat.QuarterID = Quarter.QuarterID) " \
                      f"WHERE FD_ID = {input} " \
                      f"ORDER BY year,quarter ASC;"

    pipeline = [
    {
         "$match":{    
                "RS_ID":{
                    "$exists": "true"
            },
            "RS_ID": int(resaleID)
        }
    },
    {
        "$project":{    
            "_id":0,
            "lease_commence_date": 0,
            "block": 0,
            "model": 0,
            "floor_area_sqm": 0,
            "town": 0,
            "room_type": 0,
        }
    }
    ]
    print(pipeline)
    queryStatement = col.aggregate(pipeline)
    return dumps(list(queryStatement),indent=4), 200, {'ContentType': 'application/json'}


@app.route('/pmi/all/getPropertyType' , methods = ['GET'])
def getPropertyType():  
    col = db["PropertyGeeks"]
    queryStatement = col.aggregate([{"$group": {
            "_id": "$propertyType"}}])
    return list(queryStatement) 
    # return json.dumps(output), 200, {'ContentType': 'application/json'}

@app.route('/pmi/all/getPMIByFilter' , methods = ['GET'])
def getPMIByFilter():
    pid_input = request.args.get('pid') #propertyTypeID
    proj_input = request.args.get('project') 
    street_input = request.args.get('street')
    pipeline = [
    {
        "$match":{
            "$or":[
            {
                "PRENT_ID":{
                    "$exists": "true"
            }},
            {
                "PSALE_ID":{
                    "$exists": "true"
            }}
            ],
        }
    },
    {
        "$project":{    
            "_id":0,
            "year": 0,
            "quarter": 0,
            "area(Sqm)": 0,
            "tenure": 0,
            "rent_price": 0
            
        }
    }
    ]
    if pid_input:
        pipeline[0]["$match"]["propertyType"] = pid_input
    if proj_input:
        pipeline[0]["$match"]["project"] = proj_input
    if street_input:
        pipeline[0]["$match"]["street"] = street_input
    
    queryStatement = col.aggregate(pipeline)
    return dumps(list(queryStatement),indent=4), 200, {'ContentType': 'application/json'}
    

@app.route('/pmi/filter/getPMIRental' , methods = ['GET'])
def getPMIRental():
    pmi_id = request.args.get('pmi_id')
    pipeline = [
    {
        "$match":{
            "PRENT_ID":{
                "$exists": "true"
            },
            "PRENT_ID" : pmi_id
        }
    },
    {
        "$project":{    
            "_id":0,
            "project": 0,
            "street": 0,
            "propertyType": 0,
            "typeOfArea": 0,
            "tenure": 0,
        }
    }
    ]
    queryStatement = col.aggregate(pipeline)
    return dumps(list(queryStatement),indent=4), 200, {'ContentType': 'application/json'}

@app.route('/pmi/filter/getPMISalesPrice' , methods = ['GET'])
def getPMISalesPrice():
    pmi_id = request.args.get('pmi_id')
    pipeline = [
    {
        "$match":{
            "PSALE_ID":{
                "$exists": "true"
            },
            "PSALE_ID" : pmi_id
        }
    },
    {
        "$project":{    
            "_id":0,
            "project": 0,
            "street": 0,
            "propertyType": 0,
            "typeOfArea": 0,
            "tenure": 0,
        }
    }
    ]
    queryStatement = col.aggregate(pipeline)
    return dumps(list(queryStatement),indent=4), 200, {'ContentType': 'application/json'}

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
        





if __name__ == '__main__':
    app.run(debug=1)