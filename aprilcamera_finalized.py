#                           _  _  _______              _____         _               _    _               
#       /\                 (_)| ||__   __|            |  __ \       | |             | |  (_)              
#      /  \    _ __   _ __  _ | |   | |  __ _   __ _  | |  | |  ___ | |_  ___   ___ | |_  _   ___   _ __  
#     / /\ \  | '_ \ | '__|| || |   | | / _` | / _` | | |  | | / _ \| __|/ _ \ / __|| __|| | / _ \ | '_ \ 
#    / ____ \ | |_) || |   | || |   | || (_| || (_| | | |__| ||  __/| |_|  __/| (__ | |_ | || (_) || | | |
#   /_/    \_\| .__/ |_|   |_||_|   |_| \__,_| \__, | |_____/  \___| \__|\___| \___| \__||_| \___/ |_| |_|
#             | |                               __/ |                                                     
#             |_|                              |___/                                                      

#*#*# For a better viewing experience, we strongly urge you to install the Better Comments extension #*#*#

# Modules
import cv2
from pupil_apriltags import Detector
import numpy as np

# Variables
pinkSide = int # Pink Side Variable
greenSide = int # Green Side Variable
blueSide = int # Blue Side Variable
yellowSide = int # Yellow Side Variable
avgTagDistance = int # Average AprilTag Distance Variable
tagSize = 0.16  # Size of AprilTags (in meters) #! Change needed depending on AprilTag side length
focalLength = 725  # Camera's focal length #! Calibration needed

# After detecting an AprilTag, find every side length (in pixels).
#* {side = [0, 1, 2, 3], B (Blue) = [0:255], G (Green) = [0:255], R (Red) = [0:255]}
def findSideLength(side, B, G, R):
	# Distance variable between points 1 and 2
	global pointDistance
	
	# Finding first point
	pt1 = tuple(corners[side - 1, :].astype(int))
	# Finding second point
	pt2 = tuple(corners[side, :].astype(int)) 

	# Extracts distance between pt1 and pt2
	distance = np.linalg.norm(np.array(pt2) - np.array(pt1))
	pointDistance = distance
	
	# Draws the line between pt1 and pt2
	cv2.line(frame, pt1, pt2, (B, G, R), 2)
	# Writes length at the top left
	cv2.putText(frame, f"{distance:2f} pixels", (10, (30 * side) + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (B, G, R), 2)
	# Writes tag ID on AprilTag
	cv2.putText(frame, str(tagID), (corners[0, 0].astype(int), corners[0, 1].astype(int) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# After detecting an AprilTag and finding every side length (in pixels), calculate average AprilTag distance relative to the camera
def showAverageDistance():
    # Coordinate variable representing AprilTag center
	global center 
	center = (int(np.mean(corners[:, 0])), int(np.mean(corners[:, 1])))
	
	# Calculate the average tag distance using the pink and green side
	avgTagDistance = (tagSize * focalLength) / ((pinkSide * greenSide) ** 0.5)
	# Writes distance variable in the middle of the AprilTag
	cv2.putText(frame, f"{avgTagDistance:.2f} m", (center[0] - 50, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# Detector is set to "36h11" family
detector = Detector(families = "tag36h11")

# Default Camera -> 0
cap = cv2.VideoCapture(0)

while True:
	
	# Return a frame from capture device (aka camera)
	ret, frame = cap.read()
	
	# If no frame returned -> End the program
	if not ret:
		break

	# Turn frame into grayscale to facilitate AprilTag detection
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect tags in grayscale frame
	tags = detector.detect(gray_frame)
	
	for tag in tags:
		
		# Extract corner coordinates from AprilTag
		corners = tag.corners
		# Extract tag ID
		tagID = tag.tag_id
		
		# Pink Side
		findSideLength(0, 255, 0, 255)
		pinkSide = pointDistance
		
		# Yellow Side #! (not needed)
		#// findSideLength(1, 0, 255, 255)
		#// yellowSide = pointDistance

		# Green Side
		findSideLength(2, 0, 255, 0) 
		greenSide = pointDistance
		
		# Blue Side #! (not needed)
		#// findSideLength(3, 255, 0, 0)
		#// blueSide = pointDistance

		# Refer to ln 47
		showAverageDistance()
	
	# Make window named "AprilTag Detection", with a (colored) camera frame as output
	cv2.imshow("AprilTag Detection", frame)
	
	# If "Q" key is pressed -> End the program
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

# Release camera
cap.release()

# Destroy window (ln 106)
cv2.destroyAllWindows()