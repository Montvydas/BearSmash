from flask import Flask, current_app, request
import json
import threading
from threading import Thread
import thread
from ball_tracker import TargetDetector

app = Flask(__name__)

@app.route('/')
def hello_world():
   return current_app.send_static_file('index.html')


@app.route('/hit', methods=['POST'])
def hit():
   data = request.data
   dataDict = json.loads(data)

   if dataDict["id"] == 0:
      targetDetector.capture_green()
   elif dataDict["id"] == 1:
      targetDetector.capture_purple()

   print('Hit!')
   print (dataDict)
   return 'OK'


def flask_run():
   app.run(host='0.0.0.0', port=5000, threaded=True)
   # app.run()


if __name__ == '__main__':
   # Thread(target=flask_run()).start()
   # flask_run()
   print ("Before Starting Flask")
   thread.start_new_thread(flask_run, ())

   print ("After Starting Flask")
   targetDetector = TargetDetector()
   targetDetector.setup_camera()
   targetDetector.display_view()


