from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from datetime import datetime
import pymongo
import json
import sys

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://Cluster73324:qpwoeiruty@cluster73324.dsnxfd1.mongodb.net/?retryWrites=true&w=majority")
try:
    client.server_info()
except pymongo.errors.OperationFailure as err:
    print ("Connection Not Established. Exit the system")
    sys.exit(0) 

print ("Connected Successfully")
db = client['2103_database']
col = db["ResalePMI"]

@app.route('/')
def default():
    return "Hello World"

@app.route('/all/getFlatTypes', methods= ['GET'])
def getFlatTypes():
    col = db["RentHDB"]
    queryStatement = col.aggregate([{"$group": {
            "_id": "$room_type"}}])
    return list(queryStatement) 

@app.route('/all/getQuarter' , methods = ['GET'])
def getQuarter():
    col = db["RentHDB"]
    col2 = db["RentPMI"]
    queryStatement = col.aggregate([
        {"$group": {
            "_id": {
                "year":"$year",
                "quarter": "$quarter"
        }}},
        { "$sort":{"_id.year":1,"_id.quarter":1}}
        ])
    return list(queryStatement)

if __name__ == '__main__':
    app.run(debug=1)
