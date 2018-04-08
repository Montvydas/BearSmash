from flask import Flask, current_app, request
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
   return current_app.send_static_file('index.html')


@app.route('/hit', methods=['POST'])
def hit():
   print('Hit!')
   print(request.form)

   data = request.data
   dataDict = json.loads(data)
   print (dataDict)
   return 'OK'



if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)
