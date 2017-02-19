"""
operator_interface.py
=========

This file contains the OperatorInterface class, which stores references
to controllers and also is responsible for linking commands to buttons.
"""

from bot import config
from bot.utils.buttoned_xbox_controller import ButtonedXboxController

from wpilib.buttons import JoystickButton

from bot.commands import intake, shoot, shift_drive_gear, rotate_turret, \
    climb, set_articulating_box, deposit_gear

from bot.commands import dumb_feed, dumb_shoot
from bot.subsystems.gear_manipulator import GearManipulator


class OperatorInterface():

    def __init__(self, robot):
        self.robot = robot

        self.drive_controller = ButtonedXboxController(
            config.OI_DRIVE_CONTROLLER)

        JoystickButton(self.drive_controller, config.OI_INTAKE) \
            .whileHeld(intake.Intake(self.robot))

        JoystickButton(self.drive_controller, config.OI_SHOOT) \
            .whileHeld(shoot.Shoot(self.robot))

        JoystickButton(self.drive_controller, config.OI_SHIFT) \
            .whenReleased(shift_drive_gear.ShiftDriveGear(self.robot))

        JoystickButton(self.drive_controller, config.OI_TURRET_RIGHT) \
            .whileHeld(rotate_turret.RotateTurret(
                self.robot,
                speed=rotate_turret.RotateTurret.RIGHT_SPEED))

        JoystickButton(self.drive_controller, config.OI_TURRET_LEFT) \
            .whileHeld(rotate_turret.RotateTurret(
                self.robot,
                speed=rotate_turret.RotateTurret.LEFT_SPEED))

        JoystickButton(self.drive_controller, config.OI_CLIMB) \
            .toggleWhenPressed(climb.Climb(self.robot))

        JoystickButton(self.drive_controller, config.OI_DUMB_FEED) \
            .toggleWhenPressed(dumb_feed.DumbFeed(self.robot))

        JoystickButton(self.drive_controller, config.OI_DUMB_FEED_OUT) \
            .toggleWhenPressed(dumb_feed.DumbFeed(self.robot, outtake=True))

        JoystickButton(self.drive_controller, config.OI_DUMB_SHOOT) \
            .toggleWhenPressed(dumb_shoot.DumbShoot(self.robot))

        JoystickButton(self.drive_controller, 'pov_top') \
            .whenReleased(set_articulating_box.SetArticulatingBox(
                self.robot, position=GearManipulator.ARTICULATING_BOX_UP))

        JoystickButton(self.drive_controller, 'pov_right') \
            .whenReleased(set_articulating_box.SetArticulatingBox(
                self.robot, position=GearManipulator.ARTICULATING_BOX_GEAR))

        JoystickButton(self.drive_controller, 'pov_bottom') \
            .whenReleased(set_articulating_box.SetArticulatingBox(
                self.robot, position=GearManipulator.ARTICULATING_BOX_FUEL))

        JoystickButton(self.drive_controller, 'pov_left') \
            .toggleWhenPressed(deposit_gear.DepositGear(self.robot))

    def get_drive_controller(self):
        return self.drive_controller

    def get_operator_controller(self):
        return self.operator_controller
