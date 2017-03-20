"""
shoot.py
=========
"""

from wpilib.command import Command


class Intake(Command):

    def __init__(self, robot, outtake=False):
        super().__init__()
        self.robot = robot
        self.outtake = outtake
        self.requires(self.robot.floor_intake)

    def initialize(self):
        pass

    def execute(self):
        self.robot.floor_intake.intake(self.outtake)

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        self.robot.floor_intake.stop()

    def interrupted(self):
        self.end()
