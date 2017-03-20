"""
shoot.py
=========
"""

from wpilib.command import Command

SPEED = 0.15


class RotateTurret(Command):

    RIGHT_SPEED = SPEED
    LEFT_SPEED = -SPEED

    def __init__(self, robot, speed):
        super().__init__()
        self.robot = robot
        self.speed = speed
        self.requires(self.robot.turret)

    def initialize(self):
        pass

    def execute(self):
        self.robot.turret.set_speed(self.speed)

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        self.robot.turret.stop()

    def interrupted(self):
        self.end()
