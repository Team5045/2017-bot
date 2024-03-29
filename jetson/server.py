
import sys
import time
import base64
import logging

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from gevent import monkey, Greenlet


import config
from modules.driver_vision import DriverVision
from modules.shooter_targeting import ShooterTargeting
from modules.gear_targeting import GearTargeting
from modules.network_tables import NetworkTables
from modules import cv2_polyfill

monkey.patch_all()
cv2_polyfill.polyfill()

app = Flask(__name__)
socketio = SocketIO(app)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)
logging.getLogger('nt').addHandler(stream_handler)

jetson_driver_vision = DriverVision()
targeting_modules = {
    'shooter': ShooterTargeting(),
    'gear': GearTargeting()
}

jetson_network_tables = NetworkTables()
jetson_network_tables.set_socketio(socketio)
jetson_network_tables.set_choosers([
    config.NT_STARTING_POSITION_SELECTOR,
    config.NT_AUTONOMOUS_COMMAND_SELECTOR,
    config.NT_DRIVER_DIRECTION_SELECTOR
])


# --
# DRIVER-STATION-FACING ROUTES
# --


@app.route('/')
def home():
    """Request the main dashboard screen for driver station"""
    return render_template('index.html',
                           width=config.TARGETING_CAMERA_WIDTH,
                           height=config.TARGETING_CAMERA_HEIGHT
                           )


@socketio.on('request_network_tables')
def request_network_tables():
    """Request a full update of the network tables"""
    data = jetson_network_tables.get_all_values()
    emit('network_tables_update', data)


@socketio.on('edit_network_tables')
def edit_network_tables(data):
    """Edits network tables value based on websocket request"""
    jetson_network_tables.put_value(data['key'], data['value'], data['type'])


# --
# CONTINUALLY-RUNNING FUNCTIONS
# --


def request_targeting(selected_camera):
    match = targeting_modules[selected_camera].find_target()

    if match:
        jetson_network_tables.put_value(selected_camera + '_target_found',
                                        True, 'boolean')
        jetson_network_tables.put_value(selected_camera + '_target_details',
                                        match, 'object')
    else:
        jetson_network_tables.put_value(selected_camera + '_target_found',
                                        False, 'boolean')

    continually_request_targeting()


def continually_request_targeting():
    # selected_camera = jetson_network_tables.get_value(
    #     config.NT_DRIVER_DIRECTION_SELECTOR + '/selected')
    # if not selected_camera:
    #     selected_camera = 'gear'
    selected_camera = 'shooter'

    if selected_camera:
        g = Greenlet(request_targeting, selected_camera)
        g.start_later(config.TARGETING_INTERVAL)
    else:
        g = Greenlet(continually_request_targeting)
        g.start_later(config.TARGETING_RETRY_INTERVAL)


def request_driver_vision():
    # selected_camera = jetson_network_tables.get_value(
    #     config.NT_DRIVER_DIRECTION_SELECTOR + '/selected')
    # if not selected_camera:
    #     selected_camera = 'gear'
    selected_camera = 'shooter'

    module = targeting_modules[selected_camera]

    jpeg = jetson_driver_vision.get_frame_from_targeting(module=module,
                                                         make_jpeg=True)
    socketio.emit('driver_vision', {
        'raw': 'data:image/jpeg;base64,' + base64.b64encode(jpeg),
        'timestamp': time.time()
    })

    continually_request_driver_vision()


def continually_request_driver_vision():
    if True or jetson_network_tables.get_value('dashboard_connected'):
        g = Greenlet(request_driver_vision)
        g.start_later(config.DRIVER_STREAM_INTERVAL)
    else:
        g = Greenlet(continually_request_driver_vision)
        g.start_later(config.DRIVER_STREAM_RETRY_INTERVAL)


if __name__ == '__main__':
    continually_request_targeting()
    continually_request_driver_vision()

    # Allow custom port
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = config.PORT

    socketio.run(app, host=config.HOST, port=port)
