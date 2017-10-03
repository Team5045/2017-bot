"""
shooter.py
=========
"""

from wpilib.command import Subsystem
from ctre.cantalon import CANTalon

from bot.commands.rotate_turret_with_controller import \
    RotateTurretWithController
from bot import config

(P, I, D, F) = (0.01, 0, 0, 0)


class Turret(Subsystem):

    MIN_LIMIT = -1
    MAX_LIMIT = 1

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        # Configure motors
        self.motor = CANTalon(config.TURRET_MOTOR)

        self.motor.enableForwardSoftLimit(False)
        self.motor.enableReverseSoftLimit(False)

        # self.motor.setControlMode(CANTalon.ControlMode.Position)
        # self.motor.setFeedbackDevice(
        #     CANTalon.FeedbackDevice.CtreMagEncoder_Absolute)
        # self.motor.enableForwardSoftLimit(True)
        # self.motor.enableReverseSoftLimit(True)
        # self.motor.setPID(P, I, D, F)

    # def reset(angle):
    #     """When at a known angle, call this to recalibrate."""

    # def get_angle(self):
    #     return self.motor.get()

    # def set_angle(self, angle):
    #     self.motor.setControlMode(CANTalon.ControlMode.Position)
    #     self.motor.setPosition(angle)

    def initDefaultCommand(self):
        """This sets the default command for the subsytem. This command
        is run whenever no other command is running on the subsystem."""
        self.setDefaultCommand(RotateTurretWithController(self.robot))

    def has_hit_limit(self):
        return False

        if self.motor.getReverseSoftLimit():
            return self.MIN_LIMIT
        elif self.motor.getForwardSoftLimit():
            return self.MAX_LIMIT
        else:
            return False

    def set(self, speed):
        print('drive turret', speed)
        self.motor.setControlMode(CANTalon.ControlMode.PercentVbus)
        self.motor.set(speed)

    # Alias
    set_speed = set

    def stop(self):
        self.motor.set(0)
