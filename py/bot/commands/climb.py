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
        print('init climb')

    def execute(self):
        self.robot.climber.climb()

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        self.robot.climber.stop()

    def interrupted(self):
        self.end()
