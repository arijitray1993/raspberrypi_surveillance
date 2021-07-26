import flask
from flask import Flask, request, send_from_directory, jsonify
from flask import Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
import time

#flask init stuff
app = Flask(__name__, static_url_path='')
app._static_folder = "static/"
CORS(app)
app.config['SECRET_KEY'] = 'secret-key-goes-here'


class RobotState:
    state = dict()
    state['requested'] = 0
    state['data'] = None
    state['instruction'] = None
    state['statusText'] = "contacting robot..."
    state['statusUpdated'] = False
    def log_requestforim(self, instruction):
        self.state['instruction'] = instruction
        self.state['requested'] = 1

robotstate = RobotState()

@app.route("/", methods=['GET', "POST"])
def root():
    return send_from_directory("./templates/", "index.html")

@app.route("/request_robot", methods=['GET', "POST"])
def request_robot():
    if request.method=="POST":
        direction = request.form.get('direction')
        light = request.form.get('light')

        if direction!=None:
            #robotstate.state['statusText'] = "requesting robot to execute instruction..."
            #robotstate.state['statusUpdated'] = True
            robotstate.log_requestforim({'robot': direction})            
            while robotstate.state['requested']!=0:
                _=1
        
        elif light!=None:
            #robotstate.state['statusText'] = "attempting to control light ..."
            #robotstate.state['statusUpdated'] = True
            robotstate.log_requestforim({'light': light})   
            while robotstate.state['requested']!=0:
                _=1
        else:
            robotstate.log_requestforim({'status': None})
            while robotstate.state['requested']!=0:
                _=1
        
        return jsonify(robotstate.state['data'])


@app.route('/get_state', methods=['GET', 'POST'])
def get_state():
    while robotstate.state['requested']!=1:
        _=1
    #robotstate.state['statusText'] = "Request sent, processing..."
    #robotstate.state['statusUpdated'] = True
    return jsonify(robotstate.state['instruction'])


@app.route('/get_statustext', methods=['GET', 'POST'])
def get_status():
    print("waiting")
    while(robotstate.state['statusUpdated']!=True):
        _=1
    #time.sleep(1)
    robotstate.state['statusUpdated'] = False
    print("sending to html")
    print(robotstate.state['statusText'])
    return jsonify(robotstate.state['statusText'])



@app.route('/update_state', methods=['GET', 'POST'])
def update_state():
    #print(request)
    if request.method=="POST":
        im_file = request.files.get('data')
        print(im_file)
        if im_file:
            #filename = secure_filename(im_file.filename)
            #robotstate.state['statusText'] = "Gotten picture from robot, processing..."
            #robotstate.state['statusUpdated'] = True
            im_file.save(os.path.join("static/", "test_im.png"))

            random_id = str(uuid.uuid4())
            
            robotstate.state['data'] = "/test_im.png?"+random_id
        else:
            robot_message = request.form.get('robot')
            light_message = request.form.get('light')
            if robot_message!=None:
                print(robot_message)
                robotstate.state['data'] = "Robot: "+robot_message
            if light_message!=None:
                print(light_message)
                robotstate.state['data'] += "\nLight: "+light_message
            print(robotstate.state['data'])
        robotstate.state['requested'] = 0

        return jsonify("ok")

@app.route('/update_bot_status', methods=['GET', 'POST'])
def update_bot_status():
    #print(request)
    if request.method=="POST":
        robot_message = request.form.get('robot')
        light_message = request.form.get('light')
        if robot_message!=None:
            print(robot_message)
            robotstate.state['statusText'] = "Robot: "+robot_message
        if light_message!=None:
            print(light_message)
            robotstate.state['statusText'] += "\nLight: "+light_message
        #time.sleep(1)
        robotstate.state['statusUpdated'] = True
        return jsonify("ok")

if __name__=="__main__":
    app.run(host='0.0.0.0', port=80)






