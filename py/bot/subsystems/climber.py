from wpilib.command import Subsystem
from ctre.cantalon import CANTalon

from bot import config


class Climber(Subsystem):

    SPEED = 1

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        # Configure motors
        self.motor = CANTalon(config.CLIMBER_MOTOR)
        self.motor.reverseOutput(True)
        self.motor.setInverted(True)

    def climb(self):
        self.motor.set(self.SPEED)

    def stop(self):
        self.motor.set(0)
