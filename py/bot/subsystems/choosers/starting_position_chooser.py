from bot.utils.chooser import Chooser
from bot import config


class StartingPositionChooser(Chooser):

    KEY = config.MISC_STARTING_POSITION_DASHBOARD_KEY
    OPTIONS = ['center_airship', 'left_airship', 'right_airship']
