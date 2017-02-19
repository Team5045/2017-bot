from wpilib.command import Command

from bot import config


class ShiftDriveGear(Command):

    def __init__(self, robot, gear=None):
        super().__init__()
        self.robot = robot
        self.gear = gear
        self.requires(self.robot.drive_train)
        self.requires(self.robot.jetson)

    def initialize(self):
        # If a particular gear is passed, shift to that
        if self.gear:
            self.robot.drive_train.set_gear(self.gear)
            return

        # Otherwise toggle
        current_gear = self.robot.drive_train.get_gear()
        if current_gear == self.robot.drive_train.LOW_GEAR:
            self.robot.drive_train.set_gear(self.robot.drive_train.HIGH_GEAR)
        else:
            self.robot.drive_train.set_gear(self.robot.drive_train.LOW_GEAR)

    def isFinished(self):
        return True

    def end(self):
        # Update gear displayed in dashboard

        if self.robot.drive_train.get_gear() == \
                self.robot.drive_train.LOW_GEAR:
            gear = 'LOW_GEAR'
        else:
            gear = 'HIGH_GEAR'

        self.robot.jetson.put_value(config.MISC_DRIVE_GEAR_DASHBOARD_KEY,
                                    gear,
                                    valueType='string')

    def interrupted(self):
        self.end()
