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

DEBUG = True


class DriveTrain(Subsystem):

    TANK_MODE = 1
    ARCADE_MODE = 2
    JAMES_MODE = 3

    DRIVE_MODE = ARCADE_MODE

    HIGH_GEAR = 2
    LOW_GEAR = 1

    DRIVE_TOLERANCE = 0.5  # Inches
    ROTATE_TOLERANCE = 0.2  # Degrees

    DRIVE_PROFILE = 0
    # DRIVE_PIDF = (0.8, 0, 0, 0)
    DRIVE_PIDF = (0.04, 0.05, 0, 0, 1000)  # debugging but poss hardware issue
    DRIVE_PIDF_WHEN_CLOSE = (0.8, 0, 0, 0, 0)
    DRIVE_CLOSE_TOLERANCE = 12  # Shift when <12 in.

    ROTATE_PROFILE = 1
    # ROTATE_PIDF = (10, 0, 50, 0)
    ROTATE_PIDF = (10, 0.01, 50, 0, 50)  # debugging but poss hardware issue
    ROTATE_MAX_SPEED = 0.6

    MAX_VOLTAGE = 12
    NOMINAL_VOLTAGE = 0

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
        self.drive_train.setSafetyEnabled(False)  # yeah fuck that

        # Configure encoders
        for motor in [self.left_motor_master, self.right_motor_master]:
            motor.setFeedbackDevice(CANTalon.FeedbackDevice.QuadEncoder)
            motor.configEncoderCodesPerRev(config.DRIVE_ENCODER_CODE_PER_REV)
            motor.setPID(*self.DRIVE_PIDF, profile=self.DRIVE_PROFILE)
            motor.setPID(*self.ROTATE_PIDF, profile=self.ROTATE_PROFILE)

        if config.IS_PRACTICE_BOT:
            self.right_motor_master.reverseSensor(True)
            self.left_motor_master.reverseSensor(False)
        else:
            self.right_motor_master.reverseSensor(True)
            self.left_motor_master.reverseSensor(False)

        # Configure shifter
        self.shifter_solenoid = ControlledSolenoid(config.DRIVE_SOLENOID_A,
                                                   config.DRIVE_SOLENOID_B)

    def initDefaultCommand(self):
        """This sets the default command for the subsytem. This command
        is run whenever no other command is running on the subsystem."""
        self.setDefaultCommand(DriveWithController(self.robot))

    def reset_motors_to_open_loop(self):
        for motor in self.get_motors():
            motor.changeControlMode(CANTalon.ControlMode.PercentVbus)
            motor.configMaxOutputVoltage(self.MAX_VOLTAGE)

    def drive(self, speed, curve=0):
        self.reset_motors_to_open_loop()
        self.drive_train.drive(speed, curve)

    def drive_with_controller(self, controller):
        self.reset_motors_to_open_loop()

        # Invert direction if driver set
        driver_direction = self.robot.driver_direction_chooser \
            .get_selected()

        if self.DRIVE_MODE == self.TANK_MODE:

            left_speed = -controller.getLeftY()
            right_speed = -controller.getRightY()

            if driver_direction != 'shooter':
                self.drive_train.tankDrive(left_speed, right_speed, True)
                # print('l', left_speed, 'r', right_speed)
            else:
                self.drive_train.tankDrive(-right_speed, -left_speed, True)
                # print('l', -right_speed, 'r', -left_speed)

        elif self.DRIVE_MODE == self.ARCADE_MODE:

            move = -controller.getLeftY()
            rotate = -controller.getRightX()

            if driver_direction != 'shooter':
                self.drive_train.arcadeDrive(move, rotate)
            else:
                self.drive_train.arcadeDrive(-move, rotate)

        elif self.DRIVE_MODE == self.JAMES_MODE:

            move = -controller.getLeftY()
            rotate = -controller.getLeftX()

            if driver_direction != 'shooter':
                self.drive_train.arcadeDrive(move, rotate)
            else:
                self.drive_train.arcadeDrive(-move, rotate)

    def get_motors(self):
        return [self.left_motor_master, self.right_motor_master]

    def get_gear(self):
        return self.shifter_solenoid.get()

    def set_gear(self, gear):
        print('set gear', gear)
        self.shifter_solenoid.set(gear)

    def stop(self):
        self.drive(0)

    def set_max_speed(self, speed=1):
        """Speed: 0 - 1"""
        for motor in self.get_motors():
            motor.configMaxOutputVoltage(speed * self.MAX_VOLTAGE)

    ##############
    # AUTO DRIVE #
    ##############

    def get_encoder_distance(self):
        return config.DRIVE_ENCODER_DISTANCE_PER_REV * \
            (self.left_motor_master.getPosition() * config.ENC_LEFT_FACTOR +
            self.right_motor_master.getPosition() * config.ENC_RIGHT_FACTOR) / 2

    def get_encoder_distance_data(self):
        return [
            config.DRIVE_ENCODER_DISTANCE_PER_REV *
            self.left_motor_master.getPosition() * config.ENC_LEFT_FACTOR,
            config.DRIVE_ENCODER_DISTANCE_PER_REV *
            self.right_motor_master.getPosition() * config.ENC_RIGHT_FACTOR
        ]

    def convert_rotations_to_inches(self, rotations):
        return rotations * config.DRIVE_ENCODER_DISTANCE_PER_REV

    def convert_inches_to_rotations(self, inches):
        return inches / config.DRIVE_ENCODER_DISTANCE_PER_REV

    def convert_native_units_to_inches(self, native_units):
        return (1 / config.DRIVE_ENCODER_CODE_PER_REV) * \
            self.convert_rotations_to_inches(native_units)

    def reset_auto_drive(self):
        for motor in self.get_motors():
            motor.setPosition(0)
            motor.configMaxOutputVoltage(self.MAX_VOLTAGE)

    def auto_drive(self, distance):
        setpoint = self.convert_inches_to_rotations(distance)

        self.left_motor_master.setProfile(self.DRIVE_PROFILE)
        self.right_motor_master.setProfile(self.DRIVE_PROFILE)

        pid_to_use = self.DRIVE_PIDF_WHEN_CLOSE if self.is_auto_drive_close() \
            else self.DRIVE_PIDF
        self.left_motor_master.setPID(*pid_to_use)
        self.right_motor_master.setPID(*pid_to_use)

        self.left_motor_master.changeControlMode(
            CANTalon.ControlMode.Position)
        self.right_motor_master.changeControlMode(
            CANTalon.ControlMode.Position)

        self.left_motor_master.set(-setpoint)
        self.right_motor_master.set(-setpoint)

    def get_auto_drive_errors(self):
        def get_error(m):
            return self.convert_native_units_to_inches(m.getClosedLoopError())

        errors = [get_error(m) for m in self.get_motors()]

        if DEBUG:
            for m in self.get_motors():
                print(m.deviceNumber, 'setpoint', m.getSetpoint(), 'pos', m.getPosition(), 'RPM', m.getSpeed(),
                      'closedlooperr', m.getClosedLoopError(), 'appliedThrottle', (m.getOutputVoltage() / m.getBusVoltage()) * 1023)
            print(errors)

        return errors

    def is_auto_drive_close(self):
        for err in self.get_auto_drive_errors():
            if abs(err) < self.DRIVE_CLOSE_TOLERANCE:
                if DEBUG:
                    print('autodrive is close')
                return True
        return False

    def get_auto_drive_within_tolerance(self):
        errors = self.get_auto_drive_errors()

        for error in errors:
            if abs(error) > self.DRIVE_TOLERANCE:
                return False

        # return False
        return True

    ###############
    # AUTO ROTATE #
    ###############

    def convert_degrees_to_rotations(self, degrees):
        return degrees / config.DRIVE_ENCODER_DEGREES_PER_REV

    def convert_rotations_to_degrees(self, rotations):
        return rotations * config.DRIVE_ENCODER_DEGREES_PER_REV

    def convert_native_units_to_degrees(self, native_units):
        return (1 / config.DRIVE_ENCODER_CODE_PER_REV) * \
            self.convert_rotations_to_degrees(native_units)

    def reset_auto_rotate(self):
        for motor in self.get_motors():
            motor.setPosition(0)
            motor.configMaxOutputVoltage(
                self.ROTATE_MAX_SPEED * self.MAX_VOLTAGE)

    def auto_rotate(self, degrees):
        setpoint = self.convert_degrees_to_rotations(degrees)

        self.left_motor_master.setProfile(self.ROTATE_PROFILE)
        self.right_motor_master.setProfile(self.ROTATE_PROFILE)
        self.left_motor_master.changeControlMode(
            CANTalon.ControlMode.Position)
        self.right_motor_master.changeControlMode(
            CANTalon.ControlMode.Position)

        self.left_motor_master.set(-setpoint)
        self.right_motor_master.set(-setpoint)

    def get_auto_rotate_errors(self):
        def get_error(m):
            return self.convert_native_units_to_degrees(m.getClosedLoopError())

        errors = [get_error(m) for m in self.get_motors()]

        if DEBUG:
            for m in self.get_motors():
                print(m.deviceNumber, 'setpoint', m.getSetpoint(), 'pos', m.getPosition(), 'RPM', m.getSpeed(),
                      'closedlooperr', m.getClosedLoopError(), 'appliedThrottle', (m.getOutputVoltage() / m.getBusVoltage()) * 1023)
            print(errors)

        return errors

    def get_auto_rotate_within_tolerance(self):
        errors = self.get_auto_rotate_errors()

        for error in errors:
            if abs(error) > self.ROTATE_TOLERANCE:
                return False

        # return False
        return True
