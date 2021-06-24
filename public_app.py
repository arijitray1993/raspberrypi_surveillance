from flask import Flask, request, jsonify, send_from_directory
from picamera import PiCamera

import serial
import RPi.GPIO as GPIO
import time
import requests, json
import pdb
import uuid
import time
import os

from yeelight import discover_bulbs
from yeelight import Bulb


def move_camera(direction):
    ser.flushInput()
    print(direction)
    ser.write(direction.encode('UTF-8'))

def robot_instructions(inst):
    move_camera(inst)
    time.sleep(1.5)
    
    status_response = requests.post(url_stat_update,
                                    data={'robot':"Robot moving..."})
    cam.start_preview()
    cam.rotation=90
    cam.resolution = (320, 240)
    cam.capture("static/test_im.png")
    
    cam.stop_preview()
    
    status_response = requests.post(url_stat_update,
                                    data={'robot':"Taken picture..."})
    
    im_file = open("static/test_im.png", "rb")
    
    return im_file

def light(inst):
    
    status_response = requests.post(url_stat_update,
                                    data={'robot':"Toggling light..."})
    if bulb.get_properties()['power']=='on':
        bulb.toggle()
    else:
        bulb.toggle()
        bulb.set_brightness(85)
        
    

def execute_instruction(inst):
    
    if 'robot' in inst:
        im_file = robot_instructions(inst['robot'])
        r = requests.post(url_update, files={'data':im_file})
        
    elif 'light' in inst:
        light(inst['light'])
        im_file = robot_instructions('take_pic')
        r = requests.post(url_update, files={'data':im_file})
    else:
        light_status = bulb.get_properties()['power']
        robot_status = 'available'
        r = requests.post(url_update, data={'light': light_status,
                                            'robot':robot_status})
    
        
    

if __name__=="__main__":
    #arduino init
    ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
    ser.baudrate=9600
    robot_status="available"
    
    #picamera init
    cam = PiCamera()
    ip = discover_bulbs()[0]['ip']
    bulb = Bulb(ip)
    light_status = bulb.get_properties()['power']
    
    url_check = 'http://testapp.nautilus.optiputer.net/get_state'
    url_update = 'http://testapp.nautilus.optiputer.net/update_state'
    url_stat_update = 'http://testapp.nautilus.optiputer.net/update_bot_status'
    
    sleep_cnt = 1
    init_stage = 1
    while(True):
        try:
            if init_stage==0:
                status_response = requests.post(url_stat_update,
                                            data={'light': light_status,
                                                  'robot':robot_status})
            response = requests.get(url_check, timeout=100000)
            #print(response)
            if response.status_code == 200:
                sleep_cnt=0
                data = response.json()
                inst = data
                print(inst)
                execute_instruction(inst)
                
                light_status = bulb.get_properties()['power']
                robot_status = 'available'
                if 'status' in inst:
                    init_stage=1
                else:
                    init_stage=0
            else:
                sleep_cnt+=1
                if sleep_cnt>300:
                    sleep_cnt=300
                print("entering sleep for :"+str(sleep_cnt))
                time.sleep(sleep_cnt)
        except:
            print("something went wrong, restarting...")
    
