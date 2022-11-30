from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from datetime import datetime
<<<<<<< HEAD
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
=======
import pymongo
import json
import sys
from bson.json_util import dumps, loads

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://Cluster73324:qpwoeiruty@cluster73324.dsnxfd1.mongodb.net/?retryWrites=true&w=majority")
>>>>>>> c2be04b (update mongo)
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

# Get all the HDB types
@app.route('/flat/all/getFlatTypes', methods= ['GET'])
def getFlatTypes():
    queryStatement = col.aggregate([{"$group": {
            "_id": "$room_type"}}])
    explain_output = db.command('aggregate', 'PropertyGeeks', pipeline=([{"$group": {
            "_id": "$room_type"}}]), explain=True)

    print(explain_output)
    return list(queryStatement) 

# Get all the Quarter(HDB)
@app.route('/flat/all/getQuarter' , methods = ['GET'])
def getQuarter():
    queryStatement = col.aggregate([
        {"$match":{
            "$or":[
            {
                "RT_ID":{
                    "$ne": "null"
            }},
            {
                "PRENT_ID":{
                    "$ne": "true"
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
    if flat_type is None and region is None:
        pipeline = [
        {
            "$match":{
                "$or":[
                {
                    "RT_ID":{
                        "$ne": None
                }},
                {
                    "RS_ID":{
                        "$ne": None
                }}
                ],
            }},
            ]
    else:
        pipeline = [
        {
            "$match":{
            }},
            ]
    if flat_type:
        # pipeline[0]["$match"]["town"] = Region
        pipeline[0]["$match"]["room_type"] = flat_type
    elif region:
        pipeline[0]["$match"]["town"] = region
<<<<<<< HEAD
=======
    pipeline.append(
        {"$sort": {"price":1}}
    )
>>>>>>> c2be04b (update mongo)
    pipeline.append({
            "$project":{    
                "_id":0,
                "year":0,
                "quarter":0,
                "median_rent": 0,
            }
<<<<<<< HEAD
        })
    queryStatement = col.aggregate(pipeline)
    
    return list(queryStatement), 200, {'ContentType': 'application/json'}
=======
        }
        )
    
    print(pipeline)
    queryStatement = col.aggregate(pipeline)
    
    return dumps(list(queryStatement)), 200, {'ContentType': 'application/json'}

@app.route('/flat/all/getFlatsByFilterSort' , methods = ['GET'])
def getFlatsByFilterSort():
    region = request.args.get("region")
    if region is None:
        pipeline = [
        {
            "$match":{
                "$and":[
                {
                    "RS_ID":{
                        "$ne": None
                }},
                {
                    "price":{
                        "$ne": None
                }},
                ],
            }},
            ]
    else:
        pipeline = [
        {
            "$match":{
            }},
            ]
    if region:
        pipeline = [
        {
            "$match":{
                "$and":[
                {
                    "RS_ID":{
                        "$ne": None
                }},
                {
                    "price":{
                        "$ne": None
                }},{
                    "town":region
                }
                ],
            }},
            ]
    pipeline.append(
        {"$sort": {"price":1}}
    )
    pipeline.append({
            "$project":{    
                "_id":0,
                "year":0,
                "quarter":0,
                "median_rent": 0,
            }
        }
        )
    
    print(pipeline)
    queryStatement = col.aggregate(pipeline)
    return dumps(list(queryStatement)), 200, {'ContentType': 'application/json'}

>>>>>>> c2be04b (update mongo)

# Get HDB rental price by ID
@app.route('/flat/filter/getFlatRental' , methods = ['GET'])
def getFlatRental():
    rent_id = request.args.get("rent_id")
    pipeline = [
    {
        "$match":{
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

<<<<<<< HEAD
@app.route('/pmi/all/getPropertyType' , methods = ['GET'])
def getPropertyType():  
    queryStatement = col.aggregate([{"$group": {
            "_id": "$propertyType"}},{"$sort":{"_id":1}}])
=======

@app.route('/pmi/all/getPropertyType' , methods = ['GET'])
def getPropertyType():  
    queryStatement = col.aggregate([{"$group": {
            "_id": "$propertyType"}}])
>>>>>>> c2be04b (update mongo)
    return list(queryStatement) 

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

<<<<<<< HEAD
=======
# compare the performance for this query
>>>>>>> c2be04b (update mongo)
@app.route('/pmi/all/getPMIByFilter' , methods = ['GET'])
def getPMIByFilter():
    property_type = request.args.get('property_type') #propertyTypeID
    project = request.args.get('project') 
    street = request.args.get('street')
    if property_type is None and project is None and street is None:
        pipeline = [
        {
            "$match":{
                "$or":[
                {
                    "PRENT_ID":{
                        "$ne": "null"
                }},
                {
                    "PSALE_ID":{
                        "$ne": "null"
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
    else:
        pipeline = [
        {
            "$match":{
        }},
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
<<<<<<< HEAD
=======
    
>>>>>>> c2be04b (update mongo)


@app.route('/pmi/filter/getPMIRental' , methods = ['GET'])
def getPMIRental():
    pmi_id = request.args.get('pmi_id')
    pipeline = [
    {
        "$match":{
            "PRENT_ID":{
                "$ne": "null"
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

@app.route('/pmi/filter/getPMIRentalDetails' , methods = ['GET'])
def getPMIRentalDetails():
    pmi_id = request.args.get('pmi_id')
    pipeline = [
    {
        "$match":{
            "PRENT_ID":{
                "$ne": "null"
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

@app.route('/pmi/filter/getPMISalesPrice' , methods = ['GET'])
def getPMISalesPrice():
    pmi_id = request.args.get('pmi_id')
    pipeline = [
    {
        "$match":{
            "PSALE_ID":{
                "$ne": "null"
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

@app.route('/pmi/filter/getPMISalesDetails' , methods = ['GET'])
def getPMISalesDetails():
    pmi_id = request.args.get('pmi_id')
    pipeline = [
    {
        "$match":{
            "PSALE_ID":{
                "$ne": "null"
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

@app.route('/view/addBookmark', methods = ['POST'])
def addBookmark():
    user_id = request.args.form('user_id')
    pmi_id = request.args.form('pmi_id') or "None"
    fd_id = request.args.form('FD_ID') or "None"
    description = request.form.get('description') or ""
    haveBookMark = col.find({"user_id":user_id})
    count = len(list(haveBookMark))
    if count == 0:
        col.insert_one({
            "user_id":user_id,
            "type": "bookmark",
            "bookmarks":[
            ]
        })
    if pmi_id != "None":
        col.update_one(
            {"user_id":user_id},
            {
                "$push":{
                    "bookmarks": {
                        "pmi_id":pmi_id,
                        "description":description
                    }
                }
            }
    )
    if fd_id != "None":
        col.update_one(
            {"user_id":user_id},
            {
                "$push":{
                    "bookmarks": {
                        "fd_id":fd_id,
                        "description":description
                    }
                }
            }
    )
    return {"status":200}

@app.route('/view/removeBookmark', methods = ['POST'])
def removeBookmark():
    user_id = request.form.get('user_id')
    pmi_id = request.form.get('pmi_id') or "None"
    fd_id = request.form.get('FD_ID') or "None"
    if pmi_id != "None":
        col.update_one(
            {"user_id":user_id},
            {
                "$pull":{
                    "bookmarks": {
                        "pmi_id":pmi_id,
                    }
                }
            }
    )
    if fd_id != "None":
        col.update_one(
            {"user_id":user_id},
            {
                "$push":{
                    "bookmarks": {
                        "fd_id":fd_id,
                    }
                }
            }
    )
    return {"status":200}

@app.route('/view/getBookmark', methods = ['GET'])
def getBookmark():
    user_id = request.args.get('user_id')
    pipeline = [
    {
        "$match":{
            "type":{
                "$ne": "null"
            },
            "user_id" : user_id
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

<<<<<<< HEAD
if __name__ == '__main__':
    app.run(debug=1, port=5001)
=======

@app.route('/pmi/filter/getPMISalesAveragePrice' , methods = ['GET'])
def getPMISalesAveragePrice():
    region = request.args.get('region')
    pipeline = [
    {
    "$match":{
        "RS_ID":{
            "$ne": "null"
        },
    }
    },
    {
        "$group":{
            "_id":{
                "town": "$town",
                "averagePrice" :{"$avg": "$price"}
            # "RS_ID":{
            #     "$avg": "price"
            # }
            },
        }
    },
    ]
    queryStatement = col.aggregate(pipeline)
    return list(queryStatement), 200, {'ContentType': 'application/json'}

        

if __name__ == '__main__':
    app.run(debug=1)
    
>>>>>>> c2be04b (update mongo)
