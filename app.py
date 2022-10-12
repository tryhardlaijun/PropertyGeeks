from flask import Flask, send_from_directory, request
from flask_cors import CORS

app = Flask(__name__, static_url_path='', static_folder='frontend/public')
CORS(app)

@app.route("/", defaults={'path':''})
def serve():
    return send_from_directory(app.static_folder,'index.html')

@app.route('/flask/hello', methods=['GET','POST'])
def helloAPI():
    if request.method == 'GET':
        return {
      'resultStatus': 'SUCCESS',
      'message': "Hello GET Api Handler"
      }
    if request.method == 'POST':
        return {
      'resultStatus': 'SUCCESS',
      'message': "Hello POST Api Handler"
      }

