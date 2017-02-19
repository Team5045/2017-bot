"""
drive_train.py
=========
This file contains the drive train subsystem, which is responsible for --
you guessed it -- driving the robot.
"""

import wpilib
from wpilib.command import Subsystem
from ctre.cantalon import CANTalon

from bot import config
from bot.utils.controlled_solenoid import ControlledSolenoid
from bot.commands.drive_with_controller import DriveWithController


class DriveTrain(Subsystem):

    HIGH_GEAR = 1
    LOW_GEAR = 2

    (P, I, D, F) = (0.01, 0, 0, 0)

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        # Configure motors
        self.left_motor_master = CANTalon(
            config.DRIVE_LEFT_MOTOR_MASTER)
        self.left_motor_slave = CANTalon(
            config.DRIVE_LEFT_MOTOR_SLAVE)

        self.right_motor_master = CANTalon(
            config.DRIVE_RIGHT_MOTOR_MASTER)
        self.right_motor_slave = CANTalon(
            config.DRIVE_RIGHT_MOTOR_SLAVE)

        self.left_motor_master.setInverted(True)
        self.left_motor_master.reverseOutput(True)

        self.right_motor_master.setInverted(True)
        self.right_motor_master.reverseOutput(True)

        self.left_motor_slave.changeControlMode(CANTalon.ControlMode.Follower)
        self.left_motor_slave.set(config.DRIVE_LEFT_MOTOR_MASTER)

        self.right_motor_slave.changeControlMode(CANTalon.ControlMode.Follower)
        self.right_motor_slave.set(config.DRIVE_RIGHT_MOTOR_MASTER)

        # Configure drive train
        self.drive_train = wpilib.RobotDrive(
            self.left_motor_master,
            self.right_motor_master)

        self.drive_train.setSensitivity(config.DRIVE_SENSITIVITY)
        self.drive_train.setMaxOutput(config.DRIVE_MAX_SPEED)

        # Configure encoders
        for motor in [self.left_motor_master, self.right_motor_master]:
            motor.setFeedbackDevice(CANTalon.FeedbackDevice.QuadEncoder)
            motor.configEncoderCodesPerRev(config.DRIVE_ENCODER_CODE_PER_REV)

        # Configure shifter
        self.shifter_solenoid = ControlledSolenoid(config.DRIVE_SOLENOID_A,
                                                   config.DRIVE_SOLENOID_B)

    def initDefaultCommand(self):
        """This sets the default command for the subsytem. This command
        is run whenever no other command is running on the subsystem."""
        self.setDefaultCommand(DriveWithController(self.robot))

    def drive(self, speed, curve=0):
        self.drive_train.drive(speed, curve)

    def drive_with_controller(self, controller):
        # Invert direction if driver set
        driver_direction = self.robot.driver_direction_chooser \
            .get_selected()

        left_speed = -controller.getLeftY()
        right_speed = -controller.getRightY()

        print(driver_direction, 'left', left_speed, 'right', right_speed)

        if driver_direction == 'shooter':
            self.drive_train.tankDrive(left_speed, right_speed, True)
        else:
            self.drive_train.tankDrive(-right_speed, -left_speed, True)

    def get_motors(self):
        return [self.left_motor_master, self.right_motor_master]

    def get_gear(self):
        return self.shifter_solenoid.get()

    def set_gear(self, gear):
        self.shifter_solenoid.set(gear)

    def stop(self):
        self.drive(0)
