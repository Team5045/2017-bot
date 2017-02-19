from __future__ import division

import cv2
import numpy as np
import math

from targeting_grip_pipeline import Pipeline


class TargetingPipeline():
    """Wraps a GRIP pipeline and returns the actual results immediately."""

    def __init__(self, settings={}):
        self.pipeline = Pipeline()
        self.settings = settings

    def process(self, frame):
        self.pipeline.process(frame)
        contours = self.pipeline.filter_contours_output

        if len(contours) > 0:
            contours_by_area = sorted(contours, key=cv2.contourArea)

            max_contours = self.settings['max_contours']
            if max_contours:
                # Limit number of contours
                contours_by_area = contours_by_area[:max_contours]

            min_area_rects = map(cv2.minAreaRect, contours_by_area)

            rect = cv2.bitwise_or(cv2.minAreaRect, contours_by_area)

            if cv2.__version__.startswith('3'):
                box = cv2.boxPoints(rect)
            else:
                box = cv2.cv.boxPoints(rect)

            box = np.int0(box)

            # Draw box on frame for debugging/etc
            cv2.polylines(frame, [box], True, (255, 0, 0))

            result = make_target_data(box, contours_by_area, self.settings)
        else:
            result = False

        return result


def setup_capture_for_settings(settings):
    cap = cv2.VideoCapture(settings['camera_port'])
    cap.set(cv2.cv.CV_CAP_PROP_FPS, settings['fps'])
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, settings['width'])
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, settings['height'])
    cap.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, settings['brightness'])
    cap.set(cv2.cv.CV_CAP_PROP_EXPOSURE, settings['exposure'])
    return cap


def sortpts_clockwise(coords):
    by_x = sorted(coords, key=lambda c: c[0])

    left_side = [by_x[0], by_x[1]]
    top_left = max(left_side, key=lambda c: c[1])
    bottom_left = min(left_side, key=lambda c: c[1])

    right_side = [by_x[2], by_x[3]]
    top_right = max(right_side, key=lambda c: c[1])
    bottom_right = min(right_side, key=lambda c: c[1])

    return [top_left, top_right, bottom_right, bottom_left]


def dist_between_countours(contours, settings):
    # Scaled, resolution dependent distance between contours.
    # Returns either x or y distance, whichever is bigger.

    if len(contours) != 2:
        return 0

    a = cv2.boundingRect(contours[0])
    b = cv2.boundingRect(contours[1])

    if settings['distance_dimension'] == 'x':
        x_centers = [b.x + (b.width / 2), a.x + (a.width / 2)]
        x_distance = math.abs(x_centers[0] - x_centers[1]) / settings['width']
        return x_distance
    else:
        y_centers = [b.y + (b.height / 2), a.y + (a.height / 2)]
        y_distance = math.abs(y_centers[0] - y_centers[1]) / settings['height']
        return y_distance


def make_target_data(c, contours, settings):
    full_width = settings['width']
    full_height = settings['height']
    x_center = full_width / 2
    y_center = full_height / 2

    # Now convert coords to scaled [0, 1] coords, thus being
    # resolution-indendent. Resultant coords thus in the form:
    # 0
    # |
    # y   * (x, y)
    # |
    # 1
    #  0---x---1

    sorted_c = sortpts_clockwise(c)

    coords = map(lambda x, y:
                 (round(((x - x_center) / (full_width)) + 0.5, 3),
                  round((y - y_center) / (full_height) + 0.5, 3)),
                 sorted_c)

    top_left = coords[0]
    top_right = coords[1]
    bottom_right = coords[2]
    bottom_left = coords[3]

    x = 0
    y = 1

    center = [(top_right[x] + top_left[x] + bottom_right[x] +
               bottom_left[x]) / 4,
              (top_right[y] + top_left[y] + bottom_right[y] +
               bottom_left[y]) / 4]

    distance_between = dist_between_countours(contours, settings)

    return {
        'coords': [
            top_left,
            top_right,
            bottom_right,
            bottom_left
        ],
        'center': center,
        'distance_between': distance_between
    }
