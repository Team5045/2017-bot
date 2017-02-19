from .targeting_helpers import TargetingPipeline, setup_capture_for_settings

import config


class GearTargeting(object):

    def __init__(self):
        self.settings = {
            'camera_port': config.GEAR_TARGETING_CAMERA_PORT,
            'lower_hsv_bound': config.TARGETING_LOWER_HSV_BOUND,
            'upper_hsv_bound': config.TARGETING_UPPER_HSV_BOUND,
            'width': config.TARGETING_CAMERA_WIDTH,
            'height': config.TARGETING_CAMERA_HEIGHT,
            'fps': config.TARGETING_CAMERA_FPS,
            'white_balance': config.TARGETING_CAMERA_WHITE_BALANCE,
            'brightness': config.TARGETING_CAMERA_BRIGHTNESS,
            'exposure': config.TARGETING_CAMERA_EXPOSURE,
            'max_contours': 2,
            'distance_dimension': 'x'
        }

        self.last_frame = None  # For other modules to access
        self.cap = setup_capture_for_settings(self.settings)
        self.pipeline = TargetingPipeline(settings=self.settings)

    def find_target(self):
        ret, frame = self.cap.read()
        result = self.pipeline.process(frame)
        self.last_frame = frame
        return result
