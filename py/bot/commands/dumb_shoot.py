"""
shoot.py
=========
"""

from wpilib.command import Command


class DumbShoot(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        #self.requires(self.robot.shooter)

    def execute(self):
        self.robot.shooter.dumb_run_flywheel()

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        self.robot.shooter.dumb_stop_flywheel()

    def interrupted(self):
        self.end()
