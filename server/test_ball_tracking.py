from ball_tracker import TargetDetector
import time

if __name__ == "__main__":
    targetDetector = TargetDetector()
    targetDetector.setup_camera()
    targetDetector.display_view()


