from networktables import NetworkTables
from cscore import CameraServer, UsbCamera
import numpy as np

import time

import config
from shooter_targeting import ShooterTargeting


def main():
    print('!! vision.py launched !!')
    # NetworkTables.initialize(server='localhost')  # tfw u r the robot
    sd = NetworkTables.getTable('SmartDashboard')

    cs = CameraServer.getInstance()
    cs.enableLogging()

    #################
    #  GEAR CAMERA  #
    #################

    # No targeting, just vision
    gear_camera = cs.startAutomaticCapture(dev=config.GEAR_CAMERA,
                                           name='Gear Camera')
    gear_camera.setResolution(config.TARGETING_CAMERA_WIDTH,
                              config.TARGETING_CAMERA_HEIGHT)

    print('!! vision.py started capture !!')

    ####################
    #  SHOOTER CAMERA  #
    ####################

    shooter_camera = UsbCamera('Shooter Raw', config.SHOOTER_CAMERA)
    # shooter_camera = cs.startAutomaticCapture(dev=config.SHOOTER_CAMERA)
    shooter_camera.setResolution(config.TARGETING_CAMERA_WIDTH,
                                 config.TARGETING_CAMERA_HEIGHT)
    shooter_targeting = ShooterTargeting()

    # Get a CvSink. This will capture images from the camera
    # cvSink = cs.getVideo(name='cam%d' % config.SHOOTER_CAMERA)
    cvSink = cs.getVideo(camera=shooter_camera)

    # (optional) Setup a CvSource. This will send images back to the Dashboard
    outputStream = cs.putVideo('Targeting Cam',
                               config.TARGETING_CAMERA_HEIGHT,
                               config.TARGETING_CAMERA_WIDTH)

    # Allocating new images is very expensive, always try to preallocate
    img = np.zeros(shape=(config.TARGETING_CAMERA_HEIGHT,
                          config.TARGETING_CAMERA_WIDTH, 3),
                   dtype=np.uint8)

    while True:
        # Tell the CvSink to grab a frame from the camera and put it
        # in the source image.  If there is an error notify the output.
        elapsed, img = cvSink.grabFrame(img)
        if elapsed == 0:
            # Send the output the error.
            outputStream.notifyError(cvSink.getError())
            # skip the rest of the current iteration
            time.sleep(10)
            continue

        # Process
        result, processed_img = shooter_targeting.process(img)

        outputStream.putFrame(processed_img)
        if result:
            sd.putBoolean(config.TARGETING_SHOOTER_FOUND_KEY, True)
            sd.putNumberArray(config.TARGETING_SHOOTER_CENTER_KEY,
                              result['center'])
        else:
            sd.putBoolean(config.TARGETING_SHOOTER_FOUND_KEY, False)

        time.sleep(10)
