"""
shoot.py
=========
"""

from wpilib.command import Command


class Climb(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.climber)

    def initialize(self):
        self.robot.climber.climb()

    def execute(self):
        pass

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        self.robot.climber.stop()

    def interrupted(self):
        self.end()
