from flask import Flask
import RPi.GPIO as GPIO
import time
import threading
import socket

hostname=socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IPAddr = s.getsockname()[0]

GPIO.setmode(GPIO.BOARD)

resistorPin = 7

app = Flask(__name__)

@app.route('/')

def index():
    light = read_light()
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
    if light > 100:
        html += '<div class="box" style="border: 10px solid #98e5e5">Mail Detected ✉️'
    else:
        html += '<div class="box" style="border: 10px solid gray"> No Mail ❌'
    
    html += """

    <pre> """ + str(light) + """ </pre>

        </div>
    </center>
    <script>
        setInterval(function() {
            fetch('/api/v1/light')
            .then(response => response.text())
            .then(data => {
                if (data > 100) {
                    document.querySelector('.box').style.border = '10px solid #98e5e5';
                    document.querySelector('.box').innerHTML = 'Mail Detected ✉️';
                } else {
                    document.querySelector('.box').style.border = '10px solid gray';
                    document.querySelector('.box').innerHTML = 'No Mail ❌';
                }
            });
        }, 2000);
    </script>
    """
    return html

@app.route('/api/v1/light')
def light():
    return str(read_light())


def read_light():
    time.sleep(1)
    GPIO.setup(resistorPin, GPIO.OUT) # Set the resistorPin to output mode so we can charge the capacitor
    GPIO.output(resistorPin, GPIO.LOW) # Set the resistorPin to low so we can charge the capacitor
    time.sleep(0.1)
    
    GPIO.setup(resistorPin, GPIO.IN) # Set the resistorPin to input mode so we can read the voltage
    currentTime = time.time() # Get the current time
    diff = 0
    
    while(GPIO.input(resistorPin) == GPIO.LOW): # While the voltage is low keep looping until the voltage is high
        diff  = time.time() - currentTime # Get the difference between the current time and the time when the voltage was low 
        
    return (diff * 1000) # Print the time it took to charge the capacitor in milliseconds(ms)

if __name__ == '__main__':
    app.run(host=IPAddr, debug=True)