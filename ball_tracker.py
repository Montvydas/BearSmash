from collections import deque
import numpy as np
import imutils
import cv2

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# greenLower = (29, 86, 6)
# greenUpper = (64, 255, 255)

greenLower = (45, 60, 40)
greenUpper = (75, 255, 255)

yellowLower = (20, 50, 50)
yellowUpper = (25, 220, 220)

purpleLower = (150, 50, 50)
purpleUpper = (175, 220, 220)

def get_camera():
    return cv2.VideoCapture(0)

def close_camera(camera):
    camera.release()
    cv2.destroyAllWindows()

def capture_frame(camera):
    (grabbed, frame) = camera.read()
    if not grabbed:
        return
    frame = imutils.resize(frame, width=600)
    blurred = frame
    blurred = cv2.GaussianBlur(frame, (1, 1), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    maskPurple = cv2.inRange(hsv, purpleLower, purpleUpper)
    maskGreen = cv2.inRange(hsv, greenLower, greenUpper)

    maskPurple = cv2.erode(maskPurple, None, iterations=2)
    maskPurple = cv2.dilate(maskPurple, None, iterations=2)

    maskGreen = cv2.erode(maskGreen, None, iterations=2)
    maskGreen = cv2.dilate(maskGreen, None, iterations=2)

    cntsYellow = cv2.findContours(maskYellow.copy(), cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)[-2]
    centerYellow = None

    cntsGreen = cv2.findContours(maskGreen.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_SIMPLE)[-2]
    centerGreen = None

    if len(cntsYellow) > 0:
        c = max(cntsYellow, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 10:
            M = cv2.moments(c)
            centerYellow = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, centerYellow, 5, (0, 0, 255), -1)
            centerYellow = (centerYellow[0], centerYellow[1], radius)

    if len(cntsGreen) > 0:
        c = max(cntsGreen, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 10:
            M = cv2.moments(c)
            centerGreen = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, centerGreen, 5, (0, 0, 255), -1)
            centerGreen = (centerGreen[0], centerGreen[1], radius)

    return centerYellow, centerGreen


locationX = 150
locationY = 175
speedX = 1
speedY = 1
timer = 60

if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    pts = deque(maxlen=0)

    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()

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

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        maskPurple = cv2.inRange(hsv, purpleLower, purpleUpper)
        maskGreen = cv2.inRange(hsv, greenLower, greenUpper)

        maskPurple = cv2.erode(maskPurple, None, iterations=2)
        maskPurple = cv2.dilate(maskPurple, None, iterations=2)

        maskGreen = cv2.erode(maskGreen, None, iterations=2)
        maskGreen = cv2.dilate(maskGreen, None, iterations=2)

        cntsPurple = cv2.findContours(maskPurple.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        centerPurple = None

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cntsGreen = cv2.findContours(maskGreen.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        centerGreen = None

        if locationX > 600 - 150:
            speedX = -1
        elif locationX < 150:
            speedX = 1

        locationX += speedX

        cv2.circle(frame, (locationX, locationY), 100, (0, 0, 255), -1)
        cv2.circle(frame, (locationX, locationY), 20, (255, 255, 255), -1)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(timer), (10, 50), font, 2, (255, 255, 255), 2, cv2.CV_AA)

        # only proceed if at least one contour was found
        if len(cntsPurple) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cntsPurple, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            # only proceed if the radius meets a minimum size
            if radius > 10:
                M = cv2.moments(c)
                centerPurple = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, centerPurple, 5, (255, 255, 255), -1)
                # print center

        # only proceed if at least one contour was found
        if len(cntsGreen) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cntsGreen, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            # only proceed if the radius meets a minimum size
            if radius > 10:
                M = cv2.moments(c)
                centerGreen = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 0), 2)
                cv2.circle(frame, centerGreen, 5, (0, 0, 0), -1)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
