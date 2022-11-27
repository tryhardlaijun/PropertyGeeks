from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from datetime import datetime
from flask_cors import CORS
import pymongo
import json
import sys
import certifi
from bson.json_util import dumps, loads

app = Flask(__name__)
CORS(app)
ca = certifi.where()
client = pymongo.MongoClient("mongodb+srv://Cluster73324:qpwoeiruty@cluster73324.dsnxfd1.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
try:
    client.server_info()
except pymongo.errors.OperationFailure as err:
    print ("Connection Not Established. Exit the system")
    sys.exit(0) 

print ("Connected Successfully")
db = client['2103_database']
col = db["PropertyGeeks"]
# col.create_index("RT_ID")
# col.create_index("RS_ID")
# col.create_index("PRESALE_ID")
# col.create_index("PRENT_ID")
# col.create_index("room_type")
# col.create_index("town")
# col.create_index("quarter")
# col.create_index("year")
# col.create_index("PRENT_ID")
# col.create_index("property_type")
# col.create_index("street")
# col.create_index("project")

# with open('ResaleHDB_nosql.json') as file:
#     file_data = json.load(file)
# col.insert_many(file_data)

@app.route('/' , methods = ["GET"])
def default():
    return "WELCOME TO PROPERTY GEEKS"

# Get all the HDB types
@app.route('/flat/all/getFlatTypes', methods= ['GET'])
def getFlatTypes():
    queryStatement = col.aggregate([{"$group": {
            "_id": "$room_type"}}])
    return list(queryStatement) 

# Get all the Quarter(HDB)
@app.route('/flat/all/getQuarter' , methods = ['GET'])
def getQuarter():
    queryStatement = col.aggregate([
        {"$match":{
            "$or":[
            {
                "RT_ID":{
                    "$exists": "true"
            }},
            {
                "PRENT_ID":{
                    "$exists": "true"
            }}
            ],
        }},
        {"$group": {
            "_id": {
                "year":"$year",
                "quarter": "$quarter"
        }}},
        { "$sort":{"_id.year":1,"_id.quarter":1}},
        ])
    return list(queryStatement)

# Get all the Region(HDB)
@app.route('/flat/all/getRegion' , methods = ['GET'])
def getRegion():
    queryStatement = col.aggregate([
        {"$group": {
            "_id": "$town"}},
        { "$sort":{"_id.year":1,"_id.quarter":1}}
        ])
    return list(queryStatement)

# Filter the HDB by region and type
@app.route('/flat/all/getFlatsByFilter' , methods = ['GET'])
def getFlatByFilter():
    flat_type = request.args.get("flat_type")
    region = request.args.get("region")
    pipeline = [
    # {
    #     "$limit":1000,
    # },
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
    if flat_type:
        # pipeline[0]["$match"]["town"] = Region
        pipeline[0]["$match"]["room_type"] = flat_type
    elif region:
        pipeline[0]["$match"]["town"] = region
    pipeline.append({
            "$project":{    
                "_id":0,
                "year":0,
                "quarter":0,
                "median_rent": 0,
            }
        })
    queryStatement = col.aggregate(pipeline)
    return list(queryStatement), 200, {'ContentType': 'application/json'}

# Get HDB rental price by ID
@app.route('/flat/filter/getFlatRental' , methods = ['GET'])
def getFlatRental():
    rent_id = request.args.get("rent_id")
    pipeline = [
    {
        "$match":{
            "RT_ID":{
                "$exists": "true"
            },
            "RT_ID": rent_id
        }
    },
    {
        "$project":{    
            "_id":0,
            "lease_commence_date": 0,
            "block": 0,
            "model": 0,
            "floor_area_sqm":0,
            "town":0,
            "room_type":0
        }
    }
    ]
    queryStatement = col.aggregate(pipeline)
    return list(queryStatement), 200, {'ContentType': 'application/json'}

# get HDB rent details by ID
@app.route('/flat/filter/getRentFlatDetails' , methods = ['GET'])
def getRentFlatDetails():
    rent_id = request.args.get("rent_id")
    pipeline = [
    {
         "$match":{
            "RT_ID":{
                "$exists": "true"
            },
            "RT_ID": rent_id
        }
    },
    {
        "$project":{    
            "_id":0,
        }
    }
    ]
    queryStatement = col.aggregate(pipeline)
    return list(queryStatement), 200, {'ContentType': 'application/json'}

# get HDB resale details by ID
@app.route('/flat/filter/getResaleFlatDetails' , methods = ['GET'])
def getResaleFlatDetails():
    resale_id = request.args.get("resale_id")
    pipeline = [
    {
         "$match":{
                "RS_ID":{
                    "$exists": "true"
            },
            "RS_ID": int(resale_id)
        }
    },
    {
        "$project":{    
            "_id":0,
        }
    }
    ]
    queryStatement = col.aggregate(pipeline)
    return list(queryStatement), 200, {'ContentType': 'application/json'}

# Get HDB resale price by ID
@app.route('/flat/filter/getFlatPrice' , methods = ['GET'])
def getFlatPrice():
    resale_id = request.args.get("resale_id")
    pipeline = [
    {
         "$match":{    
                "RS_ID":{
                    "$exists": "true"
            },
            "RS_ID": int(resale_id)
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
    return list(queryStatement), 200, {'ContentType': 'application/json'}

@app.route('/pmi/all/getPropertyType' , methods = ['GET'])
def getPropertyType():  
    queryStatement = col.aggregate([{"$group": {
            "_id": "$propertyType"}}])
    return list(queryStatement) 

@app.route('/pmi/all/getPMIByFilter' , methods = ['GET'])
def getPMIByFilter():
    property_type = request.args.get('property_type') #propertyTypeID
    project = request.args.get('project') 
    street = request.args.get('street')
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
    if property_type:
        pipeline[0]["$match"]["propertyType"] = property_type
    if project:
        pipeline[0]["$match"]["project"] = project
    if street:
        pipeline[0]["$match"]["street"] = street
    
    queryStatement = col.aggregate(pipeline)
    return list(queryStatement), 200, {'ContentType': 'application/json'}

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
    return list(queryStatement), 200, {'ContentType': 'application/json'}

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
    return list(queryStatement), 200, {'ContentType': 'application/json'}

@app.route('/view/addBookmark', methods = ['POST'])
def addBookmark():
    user_id = request.form['user_id']
    pmi_id = request.form['PMI_ID'] or "NULL"
    fd_id = request.form['FD_ID'] or "NULL"
    description = request.form['description'] or ""
    query_statement = "INSERT INTO bookmark (description,userID,PMI_ID,FD_ID) " \
                      f"VALUES ('{description}',{user_id},{pmi_id},{fd_id});"
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
        
@app.route('/pmi/all/getStreets' , methods = ['GET'])
def getStreets():  
    queryStatement = col.aggregate([
        {"$group": {
            "_id": "$street"}}
        ])
    return list(queryStatement)

@app.route('/pmi/all/getProjects' , methods = ['GET'])
def getProjects():  
    queryStatement = col.aggregate([
        {"$group": {
            "_id": "$project"}}
        ])
    return list(queryStatement)

@app.route('/pmi/filter/getPMIRentalDetails' , methods = ['GET'])
def getPMIRentalDetails():
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
        }
    }
    ]
    queryStatement = col.aggregate(pipeline)
    return list(queryStatement), 200, {'ContentType': 'application/json'}

@app.route('/pmi/filter/getPMISalesDetails' , methods = ['GET'])
def getPMISalesDetails():
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
        }
    }
    ]
    queryStatement = col.aggregate(pipeline)
    return list(queryStatement), 200, {'ContentType': 'application/json'}

if __name__ == '__main__':
    app.run(debug=1, port=5001)