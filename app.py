from flask import Flask, request, jsonify, send_from_directory
from picamera import PiCamera

import serial
import RPi.GPIO as GPIO
import time
import requests, json
import pdb
import uuid
import time

#ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
#ser.baudrate=9600


app = Flask(__name__)
cam = PiCamera()

@app.route('/')
def initpage():
    
    return send_from_directory('./templates/','index.html')



@app.route('/updateim', methods = ['GET', 'POST'])
def update():
    
    if request.method=="POST":
        
        dir_data = request.form['direction']
        
        #move_camera(dir_data)
        time.sleep(1.5)
        random_id = str(uuid.uuid4())
        
        cam.start_preview()
        cam.rotation=90

        cam.capture("static/test_im.png")
        
        cam.stop_preview()
        
        return jsonify({'im':'static/test_im.png?'+random_id})


def move_camera(direction):
    ser.flushInput()
    print(direction)
    ser.write(direction.encode('UTF-8'))
    

if __name__=="__main__":
    app.run(debug=False, host='0.0.0.0')
    
    


