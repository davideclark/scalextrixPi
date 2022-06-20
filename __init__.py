# see https://flask.palletsprojects.com/en/2.1.x/tutorial/factory/
# To run from command line
# cd /home/david/repos/hackothon
# export FLASK_APP=flaskr
# FLASK_ENV=development
# flask run

import os
import RPi.GPIO as GPIO
import time
from flask import Flask
from flask import request
from flask import Flask, request, render_template


def create_app(test_config=None):
    # This needs to run at application close down
    # Cleans the GPIO
    GPIO.cleanup()
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Start PWM with 50% Duty Cycle
    redspeed = 0
    yellowspeed = 0

    GPIO.setmode(GPIO.BOARD)

    # Setup GPIO Pins
    GPIO.setup(12, GPIO.OUT) # Marked P18 on break out board
    GPIO.setup(32, GPIO.OUT)

    # Set PWM instance and their frequency
    pwm12 = GPIO.PWM(12, 300)
    pwm32 = GPIO.PWM(32, 300)

    pwm12.start(redspeed)
    pwm32.start(yellowspeed)

    # Car status
    @app.route('/status')
    def status():
        return 'Car yellow speed is ' + str(yellowspeed) + ' Car Red speed is ' + str(redspeed)
    
    @app.route('/')
    def hello():
        return render_template('index.html')
        
    @app.route('/stop')
    def stop():
        car = request.args.get('car') # red or yellow
        app.logger.warning('Stopping car ' + car)
        
        if car == 'red':
            pwm12.ChangeDutyCycle(0)
            redspeed = 40
        if car == 'yellow':
            pwm32.ChangeDutyCycle(0)
            yellowspeed = 40
        if car == '':
            pwm12.ChangeDutyCycle(0)
            pwm32.ChangeDutyCycle(0)
            yellowspeed = 0
            redspeed = 0
        return 'Cars stopped (fingers crossed)'

    @app.route('/start')
    def start():
        car = request.args.get('car') # red or yellow
        app.logger.warning('Starting car ' + car)
        
        if car == 'red':
            pwm12.ChangeDutyCycle(40)
            redspeed = 40
        if car == 'yellow':
            pwm32.ChangeDutyCycle(40)
            yellowspeed = 40
        if car == '':
            pwm12.ChangeDutyCycle(40)
            pwm32.ChangeDutyCycle(40)
            yellowspeed = 40
            redspeed = 40
        return 'Cars started (chocks away)'

    @app.route('/speed')
    def speed():
        car = request.args.get('car') # red or yellow
        speed = int(request.args.get('speed'))
        app.logger.warning('Setting car ' + car + ' speed to ' + str(speed))
        if car == 'red':
            pwm12.ChangeDutyCycle(speed)
            redspeed = speed
        if car == 'yellow':
            pwm32.ChangeDutyCycle(speed)
            yellowspeed = speed
        return 'Set car ' + car + ' speed to ' + str(speed)
    
#     @app.route('/burst')
#     def speed():
#         car = request.args.get('car') # red or yellow
#         // speed = int(request.args.get('speed'))
#         // app.logger.warning('Setting car ' + car + ' speed to ' + str(speed))
#         if car == 'red':
#             pwm12.ChangeDutyCycle(speed)
#             redspeed = speed
#         if car == 'yellow':
#             pwm32.ChangeDutyCycle(speed)
#             yellowspeed = speed
#         return 'Set car ' + car + ' speed to ' + str(speed)
    
    return app