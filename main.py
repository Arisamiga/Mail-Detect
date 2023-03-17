from flask import Flask
# import RPi.GPIO as GPIO
import time
import threading
import socket

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

# GPIO.setmode(GPIO.BOARD)

resistorPin = 7

mail = False

app = Flask(__name__)

@app.route('/')

def index():
    html = """
    <head>
        <title>Mail Detect</title>
        <link href='https://fonts.googleapis.com/css?family=Lexend' rel='stylesheet'>
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
            background-color: #f1f1f1;
        }
        .box {
            width: 400px;
            height: 50px;
            background-color: #fff;
            border: 1px solid #000;
            border-radius: 10px;
            margin: 0 auto;
            margin-top: 100px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            padding-top: 30px;
        }
        .title {
            font-size: 30px; 
            font-family: 'Lexend';  
        }
    </style>

    </head>
    <p>
    &nbsp;
    </p>
    <center>
        <div class="title">Mail Detecting System <br><br> Running on: <b>"""+ hostname + """</b></div>
        """
    if mail:
        html += '<div class="box" style="border: 10px solid #98e5e5">Mail Detected ✉️'
    else:
        html += '<div class="box" style="border: 10px solid gray"> No Mail ❌'
    
    html += """
        </div>
    </center>
    """
    return html

# def read_light():
#     time.sleep(1)
#     GPIO.setup(resistorPin, GPIO.OUT) # Set the resistorPin to output mode so we can charge the capacitor
#     GPIO.output(resistorPin, GPIO.LOW) # Set the resistorPin to low so we can charge the capacitor
#     time.sleep(0.1)
    
#     GPIO.setup(resistorPin, GPIO.IN) # Set the resistorPin to input mode so we can read the voltage
#     currentTime = time.time() # Get the current time
#     diff = 0
    
#     while(GPIO.input(resistorPin) == GPIO.LOW): # While the voltage is low keep looping until the voltage is high
#         diff  = time.time() - currentTime # Get the difference between the current time and the time when the voltage was low 
        
#     return (diff * 1000) # Print the time it took to charge the capacitor in milliseconds(ms)

if __name__ == '__main__':
    app.run(host=IPAddr, debug=True)