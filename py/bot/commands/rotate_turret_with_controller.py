"""
shoot.py
=========
"""

from wpilib.command import Command

MAX_SPEED = 0.75
MIN_SPEED = 0.05
DEADBAND = 0.1


class RotateTurretWithController(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.turret)

    def initialize(self):
        pass

    def execute(self):
        speed = -self.robot.oi.get_operator_controller().getRightX()
        if abs(speed) > DEADBAND:
            scaled = (MAX_SPEED - MIN_SPEED) * speed + MIN_SPEED
        else:
            scaled = 0

        self.robot.turret.set_speed(scaled)

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        self.robot.turret.stop()

    def interrupted(self):
        self.end()
