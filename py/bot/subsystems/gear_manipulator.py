"""
gear_manipulator.py
=========
"""

import wpilib
from wpilib.command import Subsystem

from bot import config


class GearManipulator(Subsystem):

    ARTICULATING_BOX_UP = 180
    ARTICULATING_BOX_GEAR = 120
    ARTICULATING_BOX_FUEL = 0

    DOOR_OPEN = 20
    DOOR_CLOSED = 90

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        # Configure motors
        self.articulating_box_servo_a = wpilib.Servo(
            config.GEAR_MANIPULATOR_ARTICULATING_BOX_SERVO_A)
        self.articulating_box_servo_b = wpilib.Servo(
            config.GEAR_MANIPULATOR_ARTICULATING_BOX_SERVO_B)

        self.door_servo = wpilib.Servo(
            config.GEAR_MANIPULATOR_DOOR_SERVO)

    def open(self):
        print('open')
        self.door_servo.set(self.DOOR_OPEN)

    def close(self):
        print('close')
        self.door_servo.set(self.DOOR_CLOSED)

    def get_articulating_box_position(self):
        return self.articulating_box_servo_a.getAngle()

    def set_articulating_box(self, position):
        print('box_pos', position)
        self.articulating_box_servo_a.setAngle(position)
        self.articulating_box_servo_b.setAngle(180 - position)
