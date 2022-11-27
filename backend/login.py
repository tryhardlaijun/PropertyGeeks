from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mariadb
from datetime import datetime
import sys

# Connect to login database
try:
    conn = mariadb.connect(
        user="bennylim",
        password="12345",
        host="Bennys-MacBook-Air.local",
        port=3306,
        database="test"
    )
except mariadb.Error as e:
    print("Error connecting to MariaDb")
    sys.exit(1)

cur = conn.cursor()


app = Flask("__name__")
app.config['SECRET_KEY'] = '12345'


@app.route('/',methods=["GET"])
def main():
    if 'username' in session:
        username = session['username']
        return jsonify({'messgae':"You are logged in", 'username': username})
    else:
        resp = jsonify({'message': 'Unauthorized'})
        passhash = generate_password_hash("12345")
        print(passhash)
        resp.status_code = 401
        return resp


@app.route('/loginAPI',methods=['POST'])
def loginAPI():
    _json = request.json
    username = _json['username']
    pwd = _json['password']
    if username and pwd:
        queryEmail = 'SELECT * FROM Login WHERE email=%s'
        cur.execute(queryEmail,(username,))
        row = cur.fetchone()
        print(row)
        if row:
            username = row[0] 
            password = row[1]
            if check_password_hash(password,pwd):
                session['username'] = username
                # cur.close()
                return jsonify({"message":"Login successfully"})
            else:
                resp = jsonify({'message':'Bad request - invalid credentials'})
                resp.status_code = 400
                return resp
        else:
            resp = jsonify({'message':'Not Found - no record found'})
            resp.status_code = 404
            return resp
    else:
        resp = jsonify({'message':'Bad request - missing credentials'})
        resp.status_code = 400
        return resp

@app.route('/logoutAPI')
def logoutAPI():
    if 'username' in session:
        session.pop('username',None)
    return jsonify({'messsage':'Succesfully logged out'})



@app.route('/registerAPI',methods=['POST'])
def registerAPI():
    _json = request.json
    email = _json["email"]
    pwd = _json["password"]
    cfPwd = _json["cfPassword"]
    firstName = _json["firstName"]
    lastName = _json["lastName"]
    phoneNumber = _json["phoneNumber"]
    # check user exist
    if email and pwd and cfPwd and firstName and phoneNumber:
        queryEmail = 'SELECT * FROM Login WHERE email=%s'
        cur.execute(queryEmail,(email,))
        rows = cur.fetchall()
        print(rows)
        if len(rows) > 0:
            resp = jsonify({'message':'Bad request - email has been used'})
            resp.status_code  = 400
            return resp
        else: #Meaning no duplicate
            if pwd == cfPwd:
                # Proceed to database insertion
                insertQuery = 'INSERT INTO Login (email,password) VALUES (%s, %s)'
                passhash = generate_password_hash(pwd)
                cur.execute(insertQuery,(email,passhash))
                conn.commit()
                return jsonify({"message":"Register successfully"})
            else:
                resp = jsonify({'message':'Bad request - Password not correct'})
                resp.status_code  = 400
                return resp
    else:
        resp = jsonify({'message':'Bad request - Fields incomplete'})
        resp.status_code  = 400
        return resp



if __name__ == '__main__':
    app.run(debug=1)
