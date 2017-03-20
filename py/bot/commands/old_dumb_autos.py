class DumbDriveForward(Autonomous):
    nickname = "Dumb drive forward"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(AutoDumbDrive(robot, time=3, speed=-0.4))


class DumbDriveForwardHighGear(CommandGroup):
    nickname = "Dumb drive forward high gear"

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.addSequential(ShiftDriveGear(robot,
                                          self.robot.drive_train.HIGH_GEAR))
        self.addSequential(AutoDumbDrive(robot, time=0.5, speed=0))
        self.addSequential(AutoDumbDrive(robot, time=3, speed=-0.4))


class DumbPlaceGear(Autonomous):
    nickname = "Dumb place gear"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(IntakeGear(robot))
        self.addSequential(AutoDumbDrive(robot, time=3, speed=-0.4))
        self.addSequential(AutoDumbDrive(robot, time=0.5, speed=0))
        self.addSequential(DepositGear(robot))
        self.addSequential(AutoDumbDrive(robot, time=0.5, speed=0))
        # self.addSequential(AutoDumbDrive(robot, time=0.25, speed=-0.4))
        self.addSequential(AutoDumbDrive(robot, time=3, speed=0.2))


class DumbPlaceAndShoot(DumbPlaceGear):
    nickname = "Dumb place and shoot"

    def __init__(self, robot):
        super().__init__(robot)
        self.addParallel(DumbShoot(robot))
        self.addParallel(RunCommandAfterTime(DumbFeed(robot), time=3))
        self.addParallel(AutoDumbDrive(robot, speed=0, dont_stop=True))


class DumbDriveAndShoot(Autonomous):
    nickname = "Dumb drive and shoot"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(IntakeGear(robot))
        self.addSequential(AutoDumbDrive(robot, time=3, speed=-0.4))
        self.addParallel(DumbShoot(robot))
        self.addParallel(RunCommandAfterTime(DumbFeed(robot), time=3))
        self.addParallel(AutoDumbDrive(robot, speed=0, dont_stop=True))


class DumbTurn(Autonomous):
    nickname = "Dumb turn"

    def __init__(self, robot):
        super().__init__(robot)
        self.addSequential(AutoRotate(robot, 90))  # Fur lols

