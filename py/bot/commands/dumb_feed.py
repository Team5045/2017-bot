"""
shoot.py
=========
"""

from wpilib.command import Command


class DumbFeed(Command):

    def __init__(self, robot, outtake=False):
        super().__init__()
        self.robot = robot
        self.outtake = outtake
        #self.requires(self.robot.shooter)

    def initialize(self):
        print('init dumb feed, outtake:', self.outtake)

    def execute(self):
        self.robot.shooter.dumb_run_feeder(self.outtake)

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        print('end dumb feed')
        self.robot.shooter.dumb_stop_feeder()

    def interrupted(self):
        self.end()
