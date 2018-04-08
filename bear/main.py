#import socket
#import wifimanager
import time
import math
from machine import I2C, Pin
import mpu6050
import socket
import urequests as requests

#server_name = "http://192.168.2.4:5000/"
server_name = "http://192.168.2.1/hit"

def http_post_socket(url):
   _,_ , host, path = url.split('/', 3)
   addr = socket.getaddrinfo(host, 5000)[0][-1]
   s = socket.socket()
   print (addr)
   s.connect(addr)
   # s.send(bytes("helloWorld"))
   s.send(bytes('POST /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
   # data = s.read()
   # print(str(data, 'utf8'), end='')
   s.close()

def http_post(value):
    response = requests.post("http://192.168.2.1:5000/hit", json={"id": 1, "value": value})
    if response.status_code != 200:
        print ("Failed to send!")
        response.close()
        return
    print ("Successfully sent!")
    response.close()

i2c = I2C(scl=Pin(16), sda=Pin(5))
accelerometer = mpu6050.accel(i2c)

t0 = time.time()
while True:
    values = accelerometer.get_values()
    a = math.sqrt(values['AcX']**2 + values['AcY']**2 + values['AcZ']**2)
    t = time.time()
    if a > 5 and t - t0 > 2:
        http_post(int(a))
        print(a)
        t0 = t
