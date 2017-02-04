"""
__init__.py
===========

The main robot class. Yay!
"""

import wpilib
from wpilib.command import Scheduler

from bot import operator_interface
from bot.subsystems import drive_train


class Robot(wpilib.IterativeRobot):

    def robotInit(self):
        """This method is run when the robot turns on. Its purpose is to
        initialize the subsystems.
        """

        self.drive_train = drive_train.DriveTrain(self)

        self.oi = operator_interface.OperatorInterface(self)

        # Set up autonomous command selector
        self.autonomous_command = None

    def autonomousInit(self):
        self.autonomous_command = self.auto_chooser.get_selected()
        self.autonomous_command.start()

    def autonomousPeriodic(self):
        Scheduler.getInstance().run()

    def teleopInit(self):
        if self.autonomous_command:
            self.autonomous_command.cancel()

    def teleopPeriodic(self):
        Scheduler.getInstance().run()

    def disabledInit(self):
        if self.autonomous_command:
            self.autonomous_command.cancel()

    def disabledPeriodic(self):
        Scheduler.getInstance().run()


if __name__ == '__main__':
    wpilib.run(Robot)
