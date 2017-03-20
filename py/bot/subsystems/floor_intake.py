"""
floor_intake.py
=========
"""

from wpilib.command import Subsystem
from ctre.cantalon import CANTalon

from bot import config


class FloorIntake(Subsystem):

    SPEED = 0.4

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        # Configure motors
        self.motor = CANTalon(config.FLOOR_INTAKE_MOTOR)
        self.motor.reverseOutput(True)
        self.motor.setInverted(True)

    def intake(self, outtake):
        self.motor.set(self.SPEED * (-1 if outtake else 1))

    def stop(self):
        self.motor.set(0)
