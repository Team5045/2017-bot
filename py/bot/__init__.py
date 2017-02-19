"""
__init__.py
===========

The main robot class. Yay!
"""

import wpilib
from wpilib.command import Scheduler

from bot import operator_interface
from bot.subsystems import drive_train, shooter, turret, climber, \
    floor_intake, gear_manipulator, compressor, jetson, navx
from bot.subsystems.choosers import driver_direction_chooser, auto_mode_chooser


class Robot(wpilib.IterativeRobot):

    def robotInit(self):
        """This method is run when the robot turns on. Its purpose is to
        initialize the subsystems.
        """

        # For testing motors
        # from utils import motor_tester
        # m = motor_tester.MotorTester()
        # m.run()

        self.jetson = jetson.Jetson(self)
        self.navx = navx.NavX(self)

        self.drive_train = drive_train.DriveTrain(self)
        self.shooter = shooter.Shooter(self)
        self.turret = turret.Turret(self)
        self.climber = climber.Climber(self)
        self.floor_intake = floor_intake.FloorIntake(self)
        self.gear_manipulator = gear_manipulator.GearManipulator(self)

        self.compressor = compressor.Compressor(self)

        self.driver_direction_chooser = driver_direction_chooser \
            .DriverDirectionChooser(self)
        self.auto_mode_chooser = auto_mode_chooser \
            .AutoModeChooser(self)

        self.oi = operator_interface.OperatorInterface(self)

        # Set up autonomous command selector
        self.autonomous_command = None

    def autonomousInit(self):
        self.autonomous_command = self.auto_mode_chooser.get_selected()
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
