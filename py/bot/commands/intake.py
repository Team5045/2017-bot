"""
shoot.py
=========
"""

from wpilib.command import Command


class Intake(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.floor_intake)

    def initialize(self):
        self.robot.floor_intake.intake()

    def execute(self):
        pass

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        self.robot.floor_intake.stop()

    def interrupted(self):
        self.end()
