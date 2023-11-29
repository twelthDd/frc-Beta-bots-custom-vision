import cv2
import numpy as np
import robotpy_apriltag as rpat

def detect_apriltags(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Create an AprilTag detector
    detector = rpat.AprilTagDetector()
    detector.addFamily("tag36h11")
    # Detect AprilTags in the grayscale frame
    detections = detector.detect(gray_frame)

    # Process each detection
    for detection in detections:
        # Get tag information  
        tag_id = detection.getId()
        x, y = detection.getCenter().x, detection.getCenter().y
        distance = detection.pose_error

        # Print the information
        print(f"[tag= {tag_id}, x= {x}, {y}, distance = {distance}]")

def main():
    # Open the camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Detect AprilTags in the captured frame
        detect_apriltags(frame)

        # Display the frame
        cv2.imshow("AprilTag Detection", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
