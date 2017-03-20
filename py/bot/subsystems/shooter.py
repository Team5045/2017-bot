"""
shooter.py
=========
"""

from wpilib.command import Subsystem
from ctre.cantalon import CANTalon

from bot import config


class Shooter(Subsystem):

    TOLERANCE = 100  # RPM
    (P, I, D, F) = (0, 0, 0, 0.311)

    FEEDER_SPEED = 1

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.flywheel_motor = CANTalon(config.SHOOTER_MOTOR)
        self.flywheel_motor.reverseOutput(True)
        self.flywheel_motor.setInverted(True)
        # self.flywheel_motor.setControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.enableLimitSwitch(False, False)
        self.flywheel_motor.clearStickyFaults()
        self.flywheel_motor.configPeakOutputVoltage(12, -12)
        self.flywheel_motor.configNominalOutputVoltage(0, -0)
        self.flywheel_motor.reverseSensor(True)

        self.flywheel_motor.setFeedbackDevice(
            CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
        self.flywheel_motor.setPID(self.P, self.I, self.D, self.F)
        self.flywheel_motor.enableControl()

        self.feeder_motor = CANTalon(config.SHOOTER_FEEDER_MOTOR)

    def set_flywheel_speed(self, speed):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.Speed)
        self.flywheel_motor.set(speed)
        # self.flywheel_motor.set(0.8)
        # print('set speed', speed)

    def get_flywheel_speed(self):
        # print('get speed', self.flywheel_motor.getSpeed())
        return self.flywheel_motor.getSpeed()

    def get_flywheel_setpoint(self):
        return self.flywheel_motor.getSetpoint()

    def get_flywheel_error(self):
        return self.flywheel_motor.getClosedLoopError()

    def is_flywheel_within_tolerance(self):
        return False
        return abs(self.flywheel_motor.getClosedLoopError()) < self.TOLERANCE

    def stop_flywheel(self):
        self.flywheel_motor.set(0)

    def dumb_run_feeder(self, outtake=False):
        self.feeder_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.feeder_motor.set(self.FEEDER_SPEED * (-1 if outtake else 1))

    def dumb_stop_feeder(self):
        self.feeder_motor.set(0)

    def dumb_run_flywheel(self, speed=0.8):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(speed)

    def dumb_stop_flywheel(self):
        self.flywheel_motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
        self.flywheel_motor.set(0)

    def stop(self):
        self.flywheel_motor.set(0)
        self.feeder_motor.set(0)
