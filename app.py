import sys
import threading
from mavlink.PrintObserver import observer
from flask import Flask, request
from flask_cors.decorator import cross_origin
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
from dotenv import dotenv_values
import time
import logging
from mavlink.Mavlink import Mavlink
from config import PASSWORD

# Init App
app = Flask(__name__, static_folder='./client/build', static_url_path='/')
CORS(app, resources={ 'r"*"': { "origins": '*' } })
socketio = SocketIO(app, cors_allowed_origins="*")

# Init mavlink
mavlink = Mavlink()

# Disable logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Videos blueprint
# app.register_blueprint(videos_blueprint, url_prefix='/api/videos')

# React app
@app.route('/')
@cross_origin()
def index():
    return app.send_static_file('index.html')

@socketio.on('disconnect')
def disconnect():
    observer.unsubscribe_handler()

# Get mavlink data
@socketio.on('getdata')
def send_message(json):
    # if json['password'] != password:
    #     return emit('error', 'Invalid password')
    return emit('data', mavlink.get_data())

# Start text
@socketio.on('test')
def start_test(json):
    if json['password'] != PASSWORD:
        return emit('error', 'Invalid Password')
    mavlink.test(json['test_type'])

@socketio.on('change_custom_mission')
def change_mission(json):
    mavlink.set_custom_mission(json['custom_mission'])

@socketio.on('getlog')
def send_log():
    return emit('log', observer.get_messages())

if __name__ == "__main__":
    print('STARTED APP')
    # def start():
    #     mavlink.execute_flight_around_zone([-22.88697155049838,  29.810392764802724])
    # thread = threading.Thread(target=start)
    # thread.start()
    socketio.run(app, host="0.0.0.0", port=5000)