"""
drive_train.py
=========

This file contains the drive train subsystem, which is responsible for --
you guessed it -- driving the robot.
"""

import wpilib
from wpilib.command import Subsystem

from bot import config
from bot.commands.drive_with_controller import DriveWithController


class DriveTrain(Subsystem):

    DRIVE_MODE = 'tank'

    def __init__(self, robot):
        super().__init__()
        self.robot = robot
		
		#Configure Motors - Expected Motor Configuration: Front Left, Front Right, Slaved Middle Motors, Slave Back Motors
		#Configure Encoder