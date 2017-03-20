from wpilib.command import Command


class AutoDrive(Command):

    MAX_SPEED = 0.4  # 0-1 scaled
    MIN_SPEED = 0.09
    TOLERANCE = .5  # Inches
    KP = 0.3
    ANGLE_KP = -0.2

    def __init__(self, robot, distance=float('inf'), speed=None,
                 dont_stop=False):
        super().__init__()
        print('init drive')
        self.robot = robot
        self.requires(self.robot.drive_train)
        self.requires(self.robot.navx)

        self.distance = abs(distance)  # Inches
        self.is_backwards = distance < 0

        self.speed = speed if speed else self.MAX_SPEED

        self.error = float('inf')
        self.angle_error = 0

        self.dont_stop = dont_stop

    def initialize(self):
        print('init autodrive')
        self.robot.drive_train.reset_encoders()
        self.robot.navx.reset()

    def execute(self):
        print('exec autodrive')
        self.angle_error = self.robot.navx.get_yaw()
        self.error = self.distance - \
            abs(self.robot.drive_train.get_encoder_distance())

        # Cap for sanity
        if self.error > 1000:
            self.error = 1000

        if self.angle_error:
            self.angle_error = (self.angle_error / 180) * 0.5

        abs_speed = abs(self.speed * self.KP * self.error)
        if abs_speed >= abs(self.speed):
            speed = self.speed * self.error / abs(self.error)
        elif abs_speed <= self.MIN_SPEED:
            speed = self.MIN_SPEED
        else:
            speed = self.speed * self.KP * self.error

        print('[auto drive]',
              'error', self.error,
              'angle error', self.angle_error,
              'speed', speed if not self.is_backwards else -speed,
              'angle', self.angle_error * self.ANGLE_KP)

        self.robot.drive_train.drive(
            speed if not self.is_backwards else -speed,
            self.angle_error * self.ANGLE_KP)

    def isFinished(self):
        print('isfin autodrive', self.error)
        if self.dont_stop:
            return False

        return abs(self.error) <= self.TOLERANCE

    def end(self):
        print('end autodrive')
        self.robot.drive_train.stop()

    def interrupted(self):
        print('interrupted auto')
        self.end()
