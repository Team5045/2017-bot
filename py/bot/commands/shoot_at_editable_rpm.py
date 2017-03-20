"""
shoot.py
=========
"""

from wpilib.command import Command

from bot import config


class ShootAtEditableRpm(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.robot.jetson.put_value(config.EDITABLE_RPM_KEY, 3000,
                                    valueType='number')

    def get_set_speed(self):
        return self.robot.jetson.get_value(config.EDITABLE_RPM_KEY,
                                           valueType='number')

    def execute(self):
        self.robot.shooter.dumb_run_flywheel(0.8)
        # desired_speed = self.get_set_speed()
        # print('desired', desired_speed)
        # self.robot.shooter.set_flywheel_speed(desired_speed)

    def isFinished(self):
        return False  # Runs until interrupted

    def end(self):
        print('end')
        self.robot.shooter.dumb_run_flywheel(0)
        #self.robot.shooter.stop_flywheel()

    def interrupted(self):
        pass
