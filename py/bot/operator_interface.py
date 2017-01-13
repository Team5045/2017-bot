"""
operator_interface.py
=========

This file contains the OperatorInterface class, which stores references
to controllers and also is responsible for linking commands to buttons.
"""

from wpilib import Joystick
from wpilib.buttons import JoystickButton, NetworkButton

from bot import config
from bot.utils.buttoned_xbox_controller import ButtonedXboxController
#from bot.commands import 

class OperatorInterface(object):

    def __init__(self, robot):
        self.robot = robot
		
    def get_drive_controller(self):
        return self.drive_controller

    def get_operator_controller(self):
        return self.operator_controller