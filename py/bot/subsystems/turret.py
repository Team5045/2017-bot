"""
shooter.py
=========
"""

from wpilib.command import Subsystem
from ctre.cantalon import CANTalon

from bot import config

MIN_ANGLE = -90
MAX_ANGLE = 90
(P, I, D, F) = (0.01, 0, 0, 0)


class Turret(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        # Configure motors
        self.motor = CANTalon(config.TURRET_MOTOR)
        self.motor.setControlMode(CANTalon.ControlMode.Position)
        self.motor.setFeedbackDevice(
            CANTalon.FeedbackDevice.CtreMagEncoder_Absolute)

        # self.motor.enableForwardSoftLimit(True)
        # self.motor.enableReverseSoftLimit(True)

        self.motor.setPID(P, I, D, F)

    def reset(angle):
        """When at a known angle, call this to recalibrate."""

    def get_angle(self):
        return self.motor.get()

    def set_angle(self, angle):
        self.motor.setControlMode(CANTalon.ControlMode.Position)
        self.motor.setPosition(angle)

    def set_speed(self, speed):
        self.motor.setControlMode(CANTalon.ControlMode.PercentVbus)
        self.motor.set(speed)

    def stop(self):
        self.motor.set(0)
