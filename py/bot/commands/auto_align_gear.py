"""
auto_align_turret.py
=========
"""

from wpilib.command import Command

TARGET_FOUND = 'gear_target_found'
TARGET_CENTER = 'gear_target_details--center'

X, Y = 0, 1  # Coordinate indices

DESIRED_X_POSITION = 0.5
DESIRED_Y_POSITION = 0.5


class AutoAlignGear(Command):

    def __init__(self, robot, search_for_target=False):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)

    def initialize(self):
        pass

    def process(self, center):
        off_x = DESIRED_X_POSITION - center[X]
        self.robot.drive_train.drive(x, angle)

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
