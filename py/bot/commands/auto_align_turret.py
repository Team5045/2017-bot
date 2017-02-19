"""
auto_align_turret.py
=========
"""

from wpilib.command import Command

TARGET_FOUND = 'shooter_target_found'
TARGET_CENTER = 'shooter_target_details--center'

X, Y = 0, 1  # Coordinate indices

DESIRED_X_POSITION = 0.45


class AutoAlignTurret(Command):

    def __init__(self, robot, search_for_target=False):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.turret)

    def initialize(self):
        pass

    def process(self, center):
        off_x = DESIRED_X_POSITION - center[X]
        self.robot.turret.set()

    def execute(self):
        if not self.robot.jetson.get_value(TARGET_FOUND, valueType='boolean'):
            if self.search_for_target:
                self.robot.turret.search()
            else:
                self.is_failed = True
                return

        else:
            coords = self.robot.jetson.get_value(TARGET_CENTER,
                                                 valueType='subarray')
            self.process(coords=coords)

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        self.robot.turret.stop()

    def interrupted(self):
        self.end()
