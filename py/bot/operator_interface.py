"""
operator_interface.py
=========

This file contains the OperatorInterface class, which stores references
to controllers and also is responsible for linking commands to buttons.
"""

from bot import config
from bot.utils.buttoned_xbox_controller import ButtonedXboxController


class OperatorInterface(object):

    def __init__(self, robot):
        self.robot = robot

        self.drive_controller = ButtonedXboxController(
            config.OI_DRIVE_CONTROLLER)

        self.operator_controller = ButtonedXboxController(
            config.OI_OPERATOR_CONTROLLER)

    def get_drive_controller(self):
        return self.drive_controller

    def get_operator_controller(self):
        return self.operator_controller
