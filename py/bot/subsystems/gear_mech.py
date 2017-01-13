"""
gear_mech.py
=========
"""

import wpilib
from wpilib.command import Subsystem

from bot import config

class GearMech(Subsystem):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        # Configure motors
        # Configure encoder