from wpilib.command import Command


class SetArticulatingBox(Command):

    def __init__(self, robot, position):
        super().__init__()
        self.robot = robot
        self.position = position
        self.requires(self.robot.gear_manipulator)

    def initialize(self):
        self.robot.gear_manipulator.set_articulating_box(self.position)

    def execute(self):
        pass

    def isFinished(self):
        return True
