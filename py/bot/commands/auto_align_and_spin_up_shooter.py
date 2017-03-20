from wpilib.command import CommandGroup

from bot.commands import auto_align_turret, run_shooter_at_needed_rpm


class AutoAlignAndSpinUpShooter(CommandGroup):

    def __init__(self, robot, initial_direction=None, stop_when_done=False):
        super().__init__(robot)

        self.robot = robot

        self.stop_when_done = stop_when_done

        self.align_command = auto_align_turret.AutoAlignTurret(
            self.robot, search_for_target=True,
            initial_direction=initial_direction)

        self.spin_up_command = run_shooter_at_needed_rpm. \
            RunShooterAtNeededRpm(self.robot)

        self.addParallel(self.align_command)
        # self.addParallel(self.spin_up_command)

    def initialize(self):
        self.is_ready = False

    def execute(self):
        # Rumble when shooter is spun up and the turret is aligned
        if self.align_command.is_within_tolerance() and \
                self.spin_up_command.is_within_tolerance():
            self.is_ready = True
            self.robot.oi.set_controller_rumble(1)

    def isFinished(self):
        if self.stop_when_done and self.is_ready:
            return True

        # Manually triggered
        return False
