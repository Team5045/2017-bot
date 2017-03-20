from __future__ import division

import cv2
# from targeting_grip_pipeline import Pipeline


def union(a, b=None):
    # print a, b
    if a and not b:
        return a

    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0] + a[2], b[0] + b[2]) - x
    h = max(a[1] + a[3], b[1] + b[3]) - y
    return (x, y, w, h)


class TargetingPipeline():
    # """Wraps a GRIP pipeline and returns the actual results immediately."""

    def __init__(self, settings={}):
        # self.pipeline = Pipeline()
        self.settings = settings

    def process(self, frame):
        # if frame is None:
        #     print "non"
        #     return False, None

        # self.pipeline.process(frame)
        # contours = self.pipeline.filter_contours_output

        # Convert to HSV color space
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)  not needed??
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # UNCOMMENT TO SHOW MASK
        # Mask to only include colors within bounds
        # frame = cv2.inRange(hsv,
        #                    self.settings['lower_hsv_bound'],
        #                    self.settings['upper_hsv_bound'])

        # contours = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,
        #                             cv2.CHAIN_APPROX_SIMPLE)[-2]

        # Mask to only include colors within bounds
        mask = cv2.inRange(hsv,
                           self.settings['lower_hsv_bound'],
                           self.settings['upper_hsv_bound'])

        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(contours) > 0:
            contours_by_area = sorted(contours,
                                      reverse=True,
                                      key=cv2.contourArea)

            # Limit number of contours
            max_contours = self.settings['max_contours']
            if max_contours:
                contours_by_area = contours_by_area[:max_contours]

            bounding_rects = map(cv2.boundingRect, contours_by_area)

            (x1, y1, w1, h1) = bounding_rects[0]
            cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1),
                          (0, 255, 0), 2)

            # Draw the second contour too
            if len(bounding_rects) > 1:
                (x2, y2, w2, h2) = bounding_rects[1]
                cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2),
                              (0, 0, 255), 2)

            (x, y, w, h) = union(*bounding_rects)
            box = ((x, y), (x, y + h), (x + w, y), (x + w, y + h))
            cv2.rectangle(frame, box[0], box[3], (255, 0, 0), 2)

            result = make_target_data(box, bounding_rects, self.settings)
        else:
            result = False

        return result, frame


def sortpts_clockwise(coords):
    by_x = sorted(coords, key=lambda c: c[0])

    left_side = [by_x[0], by_x[1]]
    top_left = max(left_side, key=lambda c: c[1])
    bottom_left = min(left_side, key=lambda c: c[1])

    right_side = [by_x[2], by_x[3]]
    top_right = max(right_side, key=lambda c: c[1])
    bottom_right = min(right_side, key=lambda c: c[1])

    return [top_left, top_right, bottom_right, bottom_left]


def dist_between_rects(rects, settings):
    # Scaled, resolution dependent distance between rectangles.
    # Returns either x or y distance, whichever is bigger.

    if len(rects) != 2:
        return 0

    (x, y, w, h) = (0, 1, 2, 3)
    (a, b) = (rects[0], rects[1])

    # print a, b

    if settings['distance_dimension'] == 'x':
        x_centers = [b[x] + (b[w] / 2), a[x] + (a[w] / 2)]
        x_distance = abs(x_centers[0] - x_centers[1]) / settings['width']
        return x_distance
    else:
        y_centers = [b[y] + (b[h] / 2), a[y] + (a[h] / 2)]
        y_distance = abs(y_centers[0] - y_centers[1]) / settings['height']
        return y_distance


def make_target_data(c, rects, settings):
    full_width = settings['width']
    full_height = settings['height']
    x_center = full_width / 2
    y_center = full_height / 2

    # print full_width, full_height, x_center, y_center

    # Now convert coords to scaled [0, 1] coords, thus being
    # resolution-indendent. Resultant coords thus in the form:
    # 0
    # |
    # y   * (x, y)
    # |
    # 1
    #  0---x---1

    sorted_c = sortpts_clockwise(c)

    coords = [(round(((x - x_center) / (full_width)) + 0.5, 3),
               round((y - y_center) / (full_height) + 0.5, 3))
              for (x, y) in sorted_c]

    # print(c, sorted_c, coords)

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

    distance_between = dist_between_rects(rects, settings)

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
