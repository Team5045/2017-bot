"""
operator_interface.py
=========

This file contains the OperatorInterface class, which stores references
to controllers and also is responsible for linking commands to buttons.
"""

from bot import config
from bot.utils.buttoned_xbox_controller import ButtonedXboxController

from wpilib.interfaces.generichid import GenericHID
from wpilib.buttons import JoystickButton

from bot.commands import intake, shift_drive_gear, \
    climb, deposit_gear, toggle_driver_direction, \
    auto_align_and_spin_up_shooter, auto_align_turret, dumb_shoot, \
    shoot_at_editable_rpm

from bot.commands import dumb_feed, increment_shooter_rpm, rotate_turret

from bot.commands import lower_gear_manipulator_plate, intake_gear, \
    deposit_gear

from bot.subsystems.gear_manipulator import GearManipulator


class OperatorInterface():

    def __init__(self, robot):
        self.robot = robot

        # DRIVE CONTROLLER

        self.drive_controller = ButtonedXboxController(
            config.OI_DRIVE_CONTROLLER)

        JoystickButton(self.drive_controller, config.OI_SHIFT) \
            .whenReleased(shift_drive_gear.ShiftDriveGear(self.robot))

        JoystickButton(self.drive_controller, config.OI_DRIVER_DIRECTION) \
            .whenReleased(
                toggle_driver_direction.ToggleDriverDirection(self.robot))

        JoystickButton(self.drive_controller, config.OI_CLIMB) \
            .toggleWhenPressed(climb.Climb(self.robot))

        JoystickButton(self.drive_controller, 'pov_bottom').whenReleased(
            lower_gear_manipulator_plate.LowerGearManipulatorPlate(self.robot))

        JoystickButton(self.drive_controller, 'pov_right') \
            .whenReleased(intake_gear.IntakeGear(self.robot))

        JoystickButton(self.drive_controller, 'pov_left') \
            .whenReleased(deposit_gear.DepositGear(self.robot))

        JoystickButton(self.drive_controller,
                       config.OI_TURRET_MANUAL_LEFT) \
            .whileHeld(
                rotate_turret.RotateTurret(
                    self.robot,
                    speed=rotate_turret.RotateTurret.LEFT_SPEED))

        JoystickButton(self.drive_controller,
                       config.OI_TURRET_MANUAL_RIGHT) \
            .whileHeld(
                rotate_turret.RotateTurret(
                    self.robot,
                    speed=rotate_turret.RotateTurret.RIGHT_SPEED))

        JoystickButton(self.drive_controller, config.OI_SHOOT_EDITABLE) \
            .toggleWhenPressed(
                dumb_shoot.DumbShoot(self.robot))

        JoystickButton(self.drive_controller, config.OI_DRIVER_INTAKE) \
            .whileHeld(dumb_feed.DumbFeed(self.robot))

        JoystickButton(self.drive_controller, config.OI_DRIVER_OUTTAKE) \
            .whileHeld(dumb_feed.DumbFeed(self.robot, outtake=True))

        # OPERATOR CONTROLLER

        self.operator_controller = ButtonedXboxController(
            config.OI_OPERATOR_CONTROLLER)

        JoystickButton(self.operator_controller, config.OI_OP_FEED_IN) \
            .whileHeld(dumb_feed.DumbFeed(self.robot))

        JoystickButton(self.operator_controller, config.OI_OP_FEED_OUT) \
            .whileHeld(dumb_feed.DumbFeed(self.robot, outtake=True))

        # JoystickButton(self.operator_controller, config.OI_OP_TURRET_LEFT) \
        #     .toggleWhenPressed(
        #         auto_align_and_spin_up_shooter.AutoAlignAndSpinUpShooter(
        #             self.robot,
        #             initial_direction=auto_align_turret.AutoAlignTurret.LEFT))

        # JoystickButton(self.operator_controller, config.OI_OP_TURRET_RIGHT) \
        #     .toggleWhenPressed(
        #         auto_align_and_spin_up_shooter.AutoAlignAndSpinUpShooter(
        #             self.robot,
        #             initial_direction=auto_align_turret.AutoAlignTurret.RIGHT))

        JoystickButton(self.operator_controller,
                       config.OI_OP_TURRET_MANUAL_LEFT) \
            .whileHeld(
                rotate_turret.RotateTurret(
                    self.robot,
                    speed=rotate_turret.RotateTurret.LEFT_SPEED))

        JoystickButton(self.operator_controller,
                       config.OI_OP_TURRET_MANUAL_RIGHT) \
            .whileHeld(
                rotate_turret.RotateTurret(
                    self.robot,
                    speed=rotate_turret.RotateTurret.RIGHT_SPEED))

        JoystickButton(self.operator_controller, config.OI_OP_SHOOT_EDITABLE) \
            .toggleWhenPressed(
                dumb_shoot.DumbShoot(self.robot))

        JoystickButton(self.operator_controller, config.OI_OP_LOWER_PLATE) \
            .whenReleased(
                lower_gear_manipulator_plate.LowerGearManipulatorPlate(
                    self.robot))

        JoystickButton(self.operator_controller, config.OI_OP_INTAKE_GEAR) \
            .whenReleased(intake_gear.IntakeGear(self.robot))

        JoystickButton(self.operator_controller, config.OI_OP_DEPOSIT_GEAR) \
            .whenReleased(deposit_gear.DepositGear(self.robot))

    def get_drive_controller(self):
        return self.drive_controller

    def get_operator_controller(self):
        return self.operator_controller

    def set_controller_rumble(self, level):
        for controller in [self.drive_controller, self.operator_controller]:
            controller.setRumble(GenericHID.RumbleType.kLeftRumble, level)
            controller.setRumble(GenericHID.RumbleType.kRightRumble, level)
