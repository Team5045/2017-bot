"""
gear_manipulator.py
=========
"""

from wpilib.command import Subsystem

from bot import config
from bot.utils.controlled_single_solenoid import ControlledSingleSolenoid


class GearManipulator(Subsystem):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.articulating_plate_solenoid = ControlledSingleSolenoid(
            config.GEAR_MANIPULATOR_ARTICULATING_PLATE_SOLENOID)
        self.cup_solenoid = ControlledSingleSolenoid(
            config.GEAR_MANIPULATOR_ARTICULATING_CUP_SOLENOID)

    def open_cup(self):
        self.cup_solenoid.deploy()

    def close_cup(self):
        self.cup_solenoid.retract()

    def raise_plate(self):
        self.articulating_plate_solenoid.retract()

    def lower_plate(self):
        self.articulating_plate_solenoid.deploy()
