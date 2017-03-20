"""
shoot.py
=========
"""

from wpilib.command import Command


class DumbShoot(Command):

    def __init__(self, robot, speed=1):
        super().__init__()
        self.robot = robot
        self.speed = speed
        #self.requires(self.robot.shooter)

    def initialize(self):
        print('init dumb shoot, speed:', self.speed)

    def execute(self):
        self.robot.shooter.dumb_run_flywheel(self.speed)

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        print('end dumb shoot')
        self.robot.shooter.dumb_stop_flywheel()

    def interrupted(self):
        self.end()
