from bot.utils.chooser import Chooser
from bot import config


class DriverDirectionChooser(Chooser):

    KEY = config.MISC_DRIVER_DIRECTION_DASHBOARD_KEY
    OPTIONS = ['gear', 'shooter']
