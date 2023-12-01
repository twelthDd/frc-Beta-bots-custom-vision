import cv2
import numpy as np
import robotpy_apriltag as rpat

def detect_and_estimate_poses(frame, estimator):
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detector = rpat.AprilTagDetector()
    detector.addFamily("tag36h11")

    detections = detector.detect(gray_frame)

    for detection in detections:

        tag_id = detection.getId()
        x, y = detection.getCenter().x, detection.getCenter().y

        pose = estimator.estimate(detection)

        translation = pose.translation()
        rotation = pose.rotation()
        roll, pitch, yaw = rotation.x_degrees, rotation.y_degrees, rotation.z_degrees

        print("-----------------------------------------------------")    
        print(f"tag = {tag_id}\nx = {x}, y = {y}\nTranslation = [{translation.x}, {translation.y}, {translation.z}]\nRotation = [{roll}, {pitch}, {yaw}]")

def main():
    cap = cv2.VideoCapture(0)
    
    tag_size = 0.1778
    fx, fy, cx, cy = 1000, 1000, 640, 480
    estimator_config = rpat.AprilTagPoseEstimator.Config(tag_size, fx, fy, cx, cy)
    estimator = rpat.AprilTagPoseEstimator(estimator_config)

    while True:

        ret, frame = cap.read()

        detect_and_estimate_poses(frame, estimator)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
