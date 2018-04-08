import numpy as np
import imutils
import cv2
import math

# greenLower = (29, 86, 6)
# greenUpper = (64, 255, 255)

greenLower = (45, 60, 40)
greenUpper = (75, 255, 255)

# yellowLower = (20, 50, 50)
# yellowUpper = (25, 220, 220)

purpleLower = (140, 40, 40)
purpleUpper = (180, 250, 250)


class TargetDetector:
    def __init__(self):
        self.camera = None
        self.count = 0
        self.init_game()

    def init_game(self):
        self.greenCount = 0
        self.purpleCount = 0
        self.captureGreen = False
        self.capturePurple = False
        self.greenScore = 0
        self.purpleScore = 0
        self.lastGreenLocation = None
        self.lastPurpleLocation = None
        self.isGameRunning = True
        self.locationX = 150
        self.locationY = 175
        self.direction = 1
        self.speedX = 0
        self.speedY = 0

    def setup_camera(self):
        self.camera = cv2.VideoCapture(0)

    def close_camera(self):
        self.camera.release()
        cv2.destroyAllWindows()

    @staticmethod
    def process_image(frame, hsv, lower, upper):
        mask = cv2.inRange(hsv, lower, upper)

        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            # only proceed if the radius meets a minimum size
            if radius > 10:
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (255, 255, 255), -1)
                # print center
                center = (center[0], center[1], radius)
        return center

    @staticmethod
    def is_within_target(target, bear):
        if target and bear:
            sqrSum = (target[0] - bear[0]) ** 2 + (target[1] - bear[1]) ** 2

            if target[2] > math.sqrt(sqrSum):
                return True
        return False

    def capture_green(self):
        self.captureGreen = True

    def capture_purple(self):
        self.capturePurple = True

    def draw_cross(self, frame, point, color):
        lineThickness = 2
        cv2.line(frame, (point[0] - 10, point[1] - 10), (point[0] + 10, point[1] + 10), color, lineThickness)
        cv2.line(frame, (point[0] - 10, point[1] + 10), (point[0] + 10, point[1] - 10), color, lineThickness)

    def display_view(self):
        while True:
            # grab the current frame
            (grabbed, frame) = self.camera.read()

            # if we are viewing a video and we did not grab a frame,
            # then we have reached the end of the video
            if not grabbed:
                break

            # resize the frame, blur it, and convert it to the HSV
            # color space
            frame = imutils.resize(frame, width=600)
            blurred = frame

            blurred = cv2.GaussianBlur(frame, (1, 1), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            # cv2.imshow("Frame", hsv)


            if self.locationX > 600 - 150:
                self.direction = -1
            elif self.locationX < 150:
                self.direction = 1

            self.speedX = max(self.purpleScore, self.greenScore) * self.direction
            self.locationX += self.speedX

            cv2.circle(frame, (self.locationX, self.locationY), 100, (0, 0, 255), -1)
            cv2.circle(frame, (self.locationX, self.locationY), 20, (255, 255, 255), -1)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, str(self.greenScore), (10, 50), font, 2, (0, 255, 0), 2, cv2.CV_AA)
            cv2.putText(frame, str(self.purpleScore), (600-100, 50), font, 2, (255, 0, 255), 2, cv2.CV_AA)

            target = (self.locationX, self.locationY, 100)

            if self.captureGreen and self.isGameRunning:
                self.greenCount += 1
                green = self.process_image(frame, hsv, greenLower, greenUpper)
                is_green = self.is_within_target(target, green)
                if is_green:
                    print "Found green!", self.count
                    self.count += 1
                    self.greenScore += 1
                    self.captureGreen = False
                    self.lastGreenLocation = green
                    # TODO in here return True
                if self.greenCount > 20:
                    self.greenCount = 0
                    self.captureGreen = False
                if self.greenCount == 1:
                    self.lastGreenLocation = green
                    # TODO in here return False

            if self.capturePurple and self.isGameRunning:
                self.purpleCount += 1
                purple = self.process_image(frame, hsv, purpleLower, purpleUpper)
                is_purple = self.is_within_target(target, purple)
                if is_purple:
                    print "Found purple!", self.count
                    self.count += 1
                    self.purpleScore += 1
                    self.capturePurple = False
                    self.lastPurpleLocation = purple
                    # TODO in here return True
                if self.purpleCount > 20:
                    self.purpleCount = 0
                    self.capturePurple = False
                if self.purpleCount == 1:
                    self.lastPurpleLocation = purple
                    # TODO in here return False

            if self.lastGreenLocation:
                self.draw_cross(frame, self.lastGreenLocation, (0, 255, 0))
            if self.lastPurpleLocation:
                self.draw_cross(frame, self.lastPurpleLocation, (255, 0, 255))

            if self.purpleScore == 10:
                cv2.putText(frame, "WINNER!", (190, 50), font, 2, (255, 0, 255), 2, cv2.CV_AA)
                self.isGameRunning = False

            if self.greenScore == 10:
                cv2.putText(frame, "WINNER!", (190, 50), font, 2, (0, 255, 0), 2, cv2.CV_AA)
                self.isGameRunning = False

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break
            if key == ord("m"):
                self.capture_purple()
                self.capture_green()
            if key == ord("n"):
                self.init_game()


        # cleanup the camera and close any open windows
        self.camera.release()
        cv2.destroyAllWindows()

# if __name__ == "__main__":
#     camera = cv2.VideoCapture(0)
#     count = 0
#
#     while True:
#         # grab the current frame
#         (grabbed, frame) = camera.read()
#
#         # if we are viewing a video and we did not grab a frame,
#         # then we have reached the end of the video
#         if not grabbed:
#             break
#
#         # resize the frame, blur it, and convert it to the HSV
#         # color space
#         frame = imutils.resize(frame, width=600)
#         blurred = frame
#
#         blurred = cv2.GaussianBlur(frame, (1, 1), 0)
#         hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
#
#         # cv2.imshow("Frame", hsv)
#
#         if locationX > 600 - 150:
#             speedX = -speed
#         elif locationX < 150:
#             speedX = speed
#
#         locationX += speedX
#
#         cv2.circle(frame, (locationX, locationY), 100, (0, 0, 255), -1)
#         cv2.circle(frame, (locationX, locationY), 20, (255, 255, 255), -1)
#
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         cv2.putText(frame, str(timer), (10, 50), font, 2, (255, 255, 255), 2, cv2.CV_AA)
#
#         green = process_image(frame, hsv, greenLower, greenUpper)
#         purple = process_image(frame, hsv, purpleLower, purpleUpper)
#
#         target = (locationX, locationY, 50)
#
#         is_green = is_within_target(target, green)
#         if is_green:
#             print "Found green!", count
#             count += 1
#
#         is_purple = is_within_target(target, purple)
#         if is_purple:
#             print "Found purple!", count
#             count += 1
#
#         cv2.imshow("Frame", frame)
#         key = cv2.waitKey(1) & 0xFF
#
#         # if the 'q' key is pressed, stop the loop
#         if key == ord("q"):
#             break
#
#     # cleanup the camera and close any open windows
#     camera.release()
#     cv2.destroyAllWindows()
