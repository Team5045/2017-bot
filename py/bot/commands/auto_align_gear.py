"""
auto_align_turret.py
=========
"""

from wpilib.command import Command

TARGET_FOUND = 'gear_target_found'
TARGET_CENTER = 'gear_target_details--center'

X, Y = 0, 1  # Coordinate indices

DESIRED_X_POSITION = 0.4
DESIRED_Y_POSITION = 0.3
CENTERING_X_TOLERANCE = 0.02
CENTERING_Y_TOLERANCE = 0.02

SPEEDS = {
    'x_mostly_y': 0.3,
    'xy': 0.4,
    'y_only': 0.3,
    'y_min': 0.1,
    'y_max': 0.3,
    'x_only': 0.5,
    'x_bounds': 0.1
}


class AutoAlignGear(Command):

    def __init__(self, robot, search_for_target=False, alignment_iterations=1):
        super().__init__()
        self.robot = robot
        self.requires(self.robot.drive_train)
        self.alignment_iterations = alignment_iterations
        self.search_for_target = search_for_target

    def initialize(self):
        self.number_of_interations_aligned = 0
        self.is_aligned = False
        self.is_failed = False

    def process(self, center):
        off_x = DESIRED_X_POSITION - center[X]
        off_y = DESIRED_X_POSITION - center[Y]

        needs_x = abs(off_x) > CENTERING_X_TOLERANCE
        needs_y = abs(off_y) > CENTERING_Y_TOLERANCE

        if (not needs_x) and (not needs_y):
            self.robot.drive_train.stop()
            self.number_of_interations_aligned += 1
            print('[auto align] iterations aligned += 1')

            if self.number_of_interations_aligned >= self.alignment_iterations:
                print('[auto align] is aligned!')
                self.is_aligned = True

            return

        if needs_x:
            speed = SPEEDS['x_mostly_y'] if abs(off_x) < 0.1 else SPEEDS['xy']
            speed = speed * ((abs(off_y) / off_y) if needs_y else 1)
            angle = 0.7 * ((abs(off_y) / off_y) if needs_y else 1)
            angle = angle * (-1 if off_x > 0 else 1)
        else:
            speed = SPEEDS['y_only'] * abs(off_y)
            speed = max(min(speed, SPEEDS['y_max']), SPEEDS['y_min'])
            speed = speed * abs(off_y) / off_y
            angle = 0

        if not needs_y:
            speed = SPEEDS['x_only'] * abs(off_x)
            speed = max(min(speed, SPEEDS['x_only'] + SPEEDS['x_bounds']),
                        SPEEDS['x_only'] - SPEEDS['x_bounds'])
            angle = abs(angle) / angle

        print('[auto align]',
              'off_x', off_x, 'off_y', off_y, 'speed', speed, 'angle', angle)

        self.robot.drive_train.drive(speed, angle)

    def execute(self):
        if not self.robot.jetson.get_value(TARGET_FOUND, valueType='boolean'):
            if self.search_for_target:
                # Just start rotating around looking for the target until we
                # find it... hehe, just keep swimming, just keep swimming.
                self.robot.drive_train.drive(0.6, -1)
            else:
                self.is_failed = True
                return

        else:
            coords = self.robot.jetson.get_value(TARGET_CENTER,
                                                 valueType='subarray')
            self.process(coords=coords)

    def isFinished(self):
        return self.is_failed or self.is_aligned

    def end(self):
        self.robot.turret.stop()

    def interrupted(self):
        self.end()
