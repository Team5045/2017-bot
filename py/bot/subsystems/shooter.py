"""
shooter.py
=========
"""

from wpilib.command import Subsystem
from ctre.cantalon import CANTalon

from bot import config


class Shooter(Subsystem):

    FLYWHEEL_SPEED = 8000  # RPM
    TOLERANCE = 100  # RPM
    (P, I, D, F) = (0.01, 0, 0, 0)

    FEEDER_SPEED = 0.5

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.motor = CANTalon(config.SHOOTER_MOTOR)
        self.motor.reverseOutput(True)
        self.motor.setInverted(True)

        self.motor.setPID(self.P, self.I, self.D, self.F)

        self.feeder_motor = CANTalon(config.SHOOTER_FEEDER_MOTOR)

    def prepare_to_shoot(self):
        self.motor.set(self.FLYWHEEL_SPEED)

    def shoot(self):
        self.motor.changeControlMode(CANTalon.ControlMode.Speed)
        self.feeder_motor.set(self.FEEDER_SPEED)

    @property
    def is_ready_to_shoot(self):
        return abs(self.get_speed() - self.FLYWHEEL_SPEED) \
            < self.TOLERANCE

    def stop(self):
        self.motor.set(0)
        self.feeder_motor.set(0)

    def get_speed(self):
        return self.motor.getSpeed()

    def dumb_run_feeder(self, outtake=False):
        self.feeder_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.feeder_motor.set(self.FEEDER_SPEED * (-1 if outtake else 1))

    def dumb_stop_feeder(self):
        self.feeder_motor.set(0)

    def dumb_run_flywheel(self):
        self.motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.motor.set(0.9)

    def dumb_stop_flywheel(self):
        self.motor.set(0)
