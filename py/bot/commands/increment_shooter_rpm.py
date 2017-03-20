"""
shoot.py
=========
"""

from wpilib.command import Command


class IncrementShooterRpm(Command):

    def __init__(self, robot, amount):
        super().__init__()
        self.robot = robot
        self.amount = amount

    def execute(self):
        self.robot.shooter.set_flywheel_speed(
            self.robot.shooter.get_flywheel_setpoint() + self.amount)

    def isFinished(self):
        return True  # Runs until interrupted

    def end(self):
        pass

    def interrupted(self):
        pass
