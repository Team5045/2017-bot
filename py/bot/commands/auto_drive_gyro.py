from wpilib.command import Command
from wpilib import PIDController

DEBUG = True


class AutoDrive(Command):

    PIDF = (0.4, 0, 0, 0)
    PIDF_CURVE = (0.005, 0, 0, 0)
    MAX_CURVE = 0.3   # max curve factor

    TOLERANCE = 0.5  # in.
    ANGLE_TOLERANCE = 1  # degrees
    TOLERANCE_BUFFER = 1  # iterations

    def __init__(self, robot, distance=float('inf'), speed=1, dont_stop=False):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)

        self.distance = distance
        self.max_speed = speed
        self.dont_stop = dont_stop

    def initialize(self):
        self.robot.drive_train.reset_auto_drive()

        self.distance_controller = PIDController(
            *self.PIDF,
            source=self.get_distance_pid_source,
            output=self.set_distance_pid_output)
        self.distance_controller.setToleranceBuffer(self.TOLERANCE_BUFFER)
        self.distance_controller.setOutputRange(-self.max_speed,
                                                self.max_speed)
        self.distance_controller.setSetpoint(self.distance)
        self.distance_controller.enable()

        self.curve_controller = PIDController(
            *self.PIDF_CURVE,
            source=self.get_curve_pid_source,
            output=self.set_curve_pid_output)
        self.curve_controller.setInputRange(-180, 180)
        self.curve_controller.setContinuous(True)
        # self.curve_controller.setToleranceBuffer(self.TOLERANCE_BUFFER)
        self.curve_controller.setOutputRange(-self.MAX_CURVE, self.MAX_CURVE)

        current_yaw = self.robot.navx.get_yaw()
        # current_yaw = self.robot.navx.get_yaw() * \
        #     (-1 if self.distance < 0 else 1)
        self.curve_controller.setSetpoint(current_yaw)  # Drive straight
        self.curve_controller.enable()

        self.speed = 0
        self.curve = 0

        # print('Initializing...')
        # Timer.delay(0.05)  # Wait for reset signal to be sent
        # self.ready_to_run = True

    def get_distance_pid_source(self):
        return self.robot.drive_train.get_encoder_distance()

    def set_distance_pid_output(self, output):
        self.speed = output

    def get_curve_pid_source(self):
        return self.robot.navx.get_yaw()
        # return self.robot.navx.get_yaw() * (-1 if self.distance < 0 else 1)

    def set_curve_pid_output(self, output):
        self.curve = output

    def execute(self):
        if DEBUG:
            print(('auto_drive#execute, pid speed: {}, avg_err: {}, ' +
                   'curve: {}, curve_err: {}').format(
                  self.speed, self.distance_controller.getError(),
                  self.curve, self.curve_controller.getError()))

        curve = -self.curve
        if self.distance < 0:
            curve *= -1

        self.robot.drive_train.drive(self.speed, curve)

    def is_on_target(self):
        return self.distance_controller.AbsoluteTolerance_onTarget(
            self.TOLERANCE)
        # return self.distance_controller.AbsoluteTolerance_onTarget(
        #     self.TOLERANCE) and \
        #     self.curve_controller.AbsoluteTolerance_onTarget(
        #         self.ANGLE_TOLERANCE)

    def isFinished(self):
        if self.dont_stop:
            return False

        return self.is_on_target()

    def end(self):
        self.distance_controller.disable()
        self.curve_controller.disable()
        self.robot.drive_train.stop()
        print('autodrive', self.distance, 'completed')

    def interrupted(self):
        self.end()
