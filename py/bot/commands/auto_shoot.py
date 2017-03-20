from wpilib.command import CommandGroup

from bot.commands import auto_align_and_spin_up_shooter, dumb_feed


class AutoShoot(CommandGroup):
    """Auto aligns the turret, spins up shooter to needed RPM, and runs
    the feeder to, like, feed balls into the shooter.
    """

    def __init__(self, robot, initial_direction=None):
        super().__init__(robot)

        self.robot = robot

        self.auto_align_and_spin_up_command = auto_align_and_spin_up_shooter. \
            AutoAlignAndSpinUpShooter(robot, initial_direction)

        self.feed_command = dumb_feed.DumbFeed(robot)

        self.addParallel(self.auto_align_and_spin_up_command)

    def initialize(self):
        self.is_ready = False

    def execute(self):
        if self.auto_align_and_spin_up_command.is_ready:
            self.feed_command.start()
        # else:
        #    self.feed_command.cancel()

    def isFinished(self):
        # Runs til end of auto
        return False
