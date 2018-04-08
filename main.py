import ball_tracker
import time

if __name__ == "__main__":
    camera = ball_tracker.get_camera()
    count = 0
    while True:
        yellow, green = ball_tracker.capture_frame(camera)
        if green and yellow:
            sqrSum = (yellow[0] - green[0]) ** 2 + (yellow[1] - green[1]) ** 2
            if (yellow[2] - green[2]) ** 2 <= sqrSum <= (yellow[2] + green[2]) ** 2:
                print "Got it!", count
                count += 1

