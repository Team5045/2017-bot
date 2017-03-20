"""
auto_align_turret.py
=========
"""

from wpilib.command import Command
from wpilib.timer import Timer

TARGET_FOUND = 'shooter_target_found'
TARGET_DISTANCE_BETWEEN = 'shooter_target_details--distance_between'

USE_ENCODER = False
DEFAULT_RPM = 3000

DUMB_SPEED = 0.7
SPIN_UP_TIMEOUT = 1


class RunShooterAtNeededRpm(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.start_time = None

    def initialize(self):
        self.start_time = Timer.getFPGATimestamp()

    def get_speed_for_distance_between(self, x):
        return DEFAULT_RPM

    def is_within_tolerance(self):
        if USE_ENCODER:
            return self.robot.shooter.is_flywheel_within_tolerance()
        else:
            return Timer.getFPGATimestamp() - self.start_time > \
                SPIN_UP_TIMEOUT

    def execute(self):
        self.robot.shooter.dumb_run_flywheel(DUMB_SPEED)
        # if not self.robot.jetson.get_value(TARGET_FOUND, valueType='boolean'):
        #     speed = DEFAULT_RPM
        # else:
        #     distance_between = self.robot.jetson.get_value(
        #         TARGET_DISTANCE_BETWEEN, valueType='number')
        #     speed = self.get_speed_for_distance_between(distance_between)

        # print('exec runshooteratneededrpm')
        # # self.robot.shooter.dumb_run_flywheel(0.8)
        # self.robot.shooter.set_flywheel_speed(speed)

    def isFinished(self):
        return False  # Keep running

    def end(self):
        print('end')
        self.robot.shooter.stop_flywheel()

    def interrupted(self):
        self.end()
