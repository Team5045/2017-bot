import config
from targeting_helpers import TargetingPipeline


class ShooterTargeting(object):

    def __init__(self):
        self.settings = {
            'lower_hsv_bound': config.TARGETING_LOWER_HSV_BOUND,
            'upper_hsv_bound': config.TARGETING_UPPER_HSV_BOUND,
            'width': config.TARGETING_CAMERA_WIDTH,
            'height': config.TARGETING_CAMERA_HEIGHT,
            'fps': config.TARGETING_CAMERA_FPS,
            'white_balance': config.TARGETING_CAMERA_WHITE_BALANCE,
            'brightness': config.TARGETING_CAMERA_BRIGHTNESS,
            'exposure': config.TARGETING_CAMERA_EXPOSURE,
            'max_contours': 2,
            'distance_dimension': 'y'
        }

        self.pipeline = TargetingPipeline(settings=self.settings)

    def process(self, frame):
        result, processed_frame = self.pipeline.process(frame)
        return result, processed_frame
