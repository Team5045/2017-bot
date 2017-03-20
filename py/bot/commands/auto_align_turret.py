"""
auto_align_turret.py
=========
"""

from wpilib.command import Command

TARGET_FOUND = 'shooter_target_found'
TARGET_CENTER = 'shooter_target_details--center'

X, Y = 0, 1  # Coordinate indices

TOLERANCE = 0.01

INITIAL_SEARCH_SPEED = 0.1
SEARCH_NORMAL_SPEED = 0.2
SEARCH_BACK_SPEED = 0.05
DESIRED_X_POSITION = 0.5
MIN_SPEED = 0.01
SPEED_MODIFIER = 0.05


class AutoAlignTurret(Command):

    RIGHT = 1
    LEFT = -1

    def __init__(self, robot, search_for_target=False, initial_direction=None):
        super().__init__()
        self.robot = robot
        self.search_for_target = search_for_target
        self.initial_direction = initial_direction
        self.requires(self.robot.turret)

    def initialize(self):
        self.error = None
        self.is_initial = True

    def search(self):
        has_hit_limit = self.robot.turret.has_hit_limit()
        if not has_hit_limit:
            has_hit_limit = 1  # Arbitrary direction

        self.robot.turret.set(has_hit_limit * SEARCH_NORMAL_SPEED)

    def process(self, center):
        print('process', center)
        has_hit_limit = self.robot.turret.has_hit_limit()

        if not has_hit_limit:
            off_x = DESIRED_X_POSITION - center[X]

            if not off_x:
                return

            direction = -(off_x / abs(off_x))
            self.error = off_x
            print('off', off_x)
            print('possible speed', direction * abs(off_x * SPEED_MODIFIER))
            self.robot.turret.set(direction * max(MIN_SPEED,
                                  abs(off_x * SPEED_MODIFIER)))
        else:
            # Search
            self.robot.turret.set(has_hit_limit * SEARCH_BACK_SPEED)

    def execute(self):
        print('exec')
        if not self.robot.jetson.get_value(TARGET_FOUND, valueType='boolean'):
            if self.initial_direction and self.is_initial:
                self.robot.turret.set(
                    self.initial_direction * INITIAL_SEARCH_SPEED)
            elif self.search_for_target:
                self.search()
            else:
                self.is_failed = True
                return

        else:
            print('process')
            self.is_initial = False
            center = self.robot.jetson.get_value(TARGET_CENTER,
                                                 valueType='subarray')
            self.process(center=center)

    def is_within_tolerance(self):
        return self.error and abs(self.error) < TOLERANCE

    def isFinished(self):
        # FIXME  FIX FIX FIX FIX
        # BEFORE COMP
        # FIX ME
        # return True # FIXME REMOVE THIS NO AUTOALIGNING RIGHT NOW
        if self.search_for_target:
            return False

        return self.is_within_tolerance()

    def end(self):
        self.robot.turret.stop()

    def interrupted(self):
        self.end()
