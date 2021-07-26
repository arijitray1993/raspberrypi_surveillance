# Rapberry Pi Surveillance Camera Tutorial 

Sample code to use your RaspberryPi for smart home controls - control YeeLight bulbs, and take pictures using your RPI Camera from anywhere. 

## RaspberryPi Setup
This code assumes RaspberryPi 4 running a 32-bit RaspberryPi 4 Linux OS.

Inside your RaspberryPi4:
- Run `git clone https://github.com/arijitray1993/raspberrypi_surveillance.git`. 
- Open `web_servo_control/web_servo_control.ino` using the ArduinoIDE and load the code into the Arduino Board. 
- Run `python public_app.py` inside a separate terminal window.

## Public Web Server Setup
This assumes you have access to an Ubuntu server that can be accessed by a public URL on which you can run a Python Flask app.
If you do not have such a server, take a look at https://www.pythonanywhere.com/. You can get a small amount of public space for free!

On the server that can run a public python app:
- `git clone https://github.com/arijitray1993/raspberrypi_surveillance.git`
- `cd public_server_interface`
- `python app.py` 


(instructions to run it locally without a public server will also be updated soon)
 







