"""
shoot.py
=========
"""

from wpilib.command import Command


class Shoot(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.shooter)

    def initialize(self):
        self.robot.shooter.prepare_to_shoot()

    def execute(self):
        if self.robot.shooter.is_ready_to_shoot:
            self.robot.shooter.shoot()
        else:
            self.robot.shooter.stop()

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        self.robot.shooter.stop()

    def interrupted(self):
        self.end()
