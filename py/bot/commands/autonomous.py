from wpilib.command import CommandGroup, WaitCommand

from bot.utils.run_command_after_time import RunCommandAfterTime
from bot.commands.deposit_gear import DepositGear
from bot.commands.intake_gear import IntakeGear
from bot.commands.auto_shoot import AutoShoot
from bot.commands.shift_drive_gear import ShiftDriveGear
from bot.commands.dumb_feed import DumbFeed
from bot.commands.dumb_shoot import DumbShoot
# from bot.commands.auto_drive import AutoDrive
from bot.commands.auto_drive_gyro import AutoDrive
# from bot.commands.auto_rotate import AutoRotate
from bot.commands.auto_rotate_gyro import AutoRotate


class Autonomous(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        # HIGH_GEAR wtf
        self.addSequential(ShiftDriveGear(robot,
                                          self.robot.drive_train.HIGH_GEAR))

    def isFinished(self):
        return super().isFinished()


class NoAutonomous(Autonomous):
    nickname = "Do nothing"

    def __init(self, robot):
        super().__init__(robot)

    def isFinished(self):
        return True


class TestDrive(Autonomous):
    nickname = "Test drive"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(AutoDrive(robot, 40, speed=0.5))


class TestDriveBackwards(Autonomous):
    nickname = "Test drive backwards"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(AutoDrive(robot, -40, speed=0.5))


class TestRotate(Autonomous):
    nickname = "Test rotate"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(AutoRotate(robot, 55))
        self.addSequential(WaitCommand(1))
        self.addSequential(AutoRotate(robot, -55))
        self.addSequential(WaitCommand(1))
        self.addSequential(AutoRotate(robot, 45))
        self.addSequential(WaitCommand(1))
        self.addSequential(AutoRotate(robot, -45))


class DriveForward(Autonomous):
    nickname = "Just drive forward"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(AutoDrive(robot, 65))


class DriveForwardAndShoot(Autonomous):
    nickname = "[FROM BOILER SIDE] Drive forward, then shoot"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(AutoDrive(robot, 65))
        self.addParallel(DumbShoot(robot))
        self.addParallel(RunCommandAfterTime(DumbFeed(robot), time=3))


class PlaceGear(Autonomous):
    nickname = "[CENTER] Drive forward, place gear"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(IntakeGear(robot))
        self.addSequential(AutoDrive(robot, 53, speed=0.5))
        # self.addSequential(AutoDrive(robot, 78, speed=0.8))
        self.addSequential(WaitCommand(0.5))
        self.addSequential(DepositGear(robot))
        # self.addSequential(AutoDrive(robot, 10))
        self.addSequential(WaitCommand(2))
        self.addSequential(AutoDrive(robot, -24, speed=0.3))


class PlaceGearAndShoot(PlaceGear):
    nickname = "[CENTER] Drive forward, place gear, shoot"

    def __init__(self, robot):
        super().__init__(robot)
        self.addParallel(DumbShoot(robot))
        self.addParallel(RunCommandAfterTime(DumbFeed(robot), time=3))


class PlaceGearLeft(Autonomous):
    nickname = "[FROM LEFT] Drive forward, place gear"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(IntakeGear(robot))
        self.addSequential(AutoDrive(robot, 47, speed=0.5))
        self.addSequential(WaitCommand(0.25))
        self.addSequential(AutoRotate(robot, 55))
        self.addSequential(WaitCommand(0.25))
        self.addSequential(AutoDrive(robot, 95, speed=0.5))
        self.addSequential(DepositGear(robot))
        self.addSequential(WaitCommand(1))
        self.addSequential(AutoDrive(robot, -24, speed=0.5))
        self.addSequential(AutoRotate(robot, -55))


class PlaceGearRight(Autonomous):
    nickname = "[FROM RIGHT] Drive forward, place gear"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(IntakeGear(robot))
        self.addSequential(AutoDrive(robot, 47, speed=0.5))
        self.addSequential(WaitCommand(0.25))
        self.addSequential(AutoRotate(robot, -55))
        self.addSequential(WaitCommand(0.25))
        self.addSequential(AutoDrive(robot, 95, speed=0.5))
        self.addSequential(DepositGear(robot))
        self.addSequential(WaitCommand(1))
        self.addSequential(AutoDrive(robot, -24, speed=0.5))
        self.addSequential(AutoRotate(robot, 55))


class ShootHopperSide(Autonomous):
    nickname = "Shoot from boiler side"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(AutoDrive(robot, 5))
        self.addParallel(DumbShoot(robot))
        self.addParallel(RunCommandAfterTime(DumbFeed(robot), time=3))


# class ShootFromHopper(Autonomous):
#     nickname = "Shoot from hopper"

#     def __init__(self, robot):
#         super().__init__(robot)
#         self.addSequential(AutoDrive(robot, 30))
#         self.addSequential(AutoRotate(robot, -90))
#         self.addSequential(AutoDrive(robot, 5))
#         self.addSequential(AutoShoot(robot))


# List of all available autonomous commands provided in file
auto_commands = [DriveForward, NoAutonomous,
                 PlaceGear, PlaceGearLeft, PlaceGearRight,
                 PlaceGearAndShoot, DriveForwardAndShoot,
                 ShootHopperSide,
                 TestRotate, TestDrive, TestDriveBackwards]

# auto_commands = [PlaceGearAndShoot]
# auto_commands = [DumbDriveForwardHighGear]
# auto_commands = [DumbPlaceGear]
# auto_commands = [DumbPlaceAndShoot]
# auto_commands = [DumbDriveForward]
# auto_commands = [DumbDriveAndShoot]
