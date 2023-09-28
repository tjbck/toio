import cv2 as cv
import numpy as np

# # Create a custom ArUco dictionary
# aruco_dict = cv2.aruco.Dictionary_create(250, 6)

# # Create parameters for the detector
# aruco_params = cv2.aruco.DetectorParameters_create()





aruco_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_ARUCO_ORIGINAL)
aruco_params =  cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(aruco_dict, aruco_params)

# Initialize the camera
cap = cv.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    if not ret:
        break

    # Detect ArUco markers
    corners, ids, rejected = detector.detectMarkers(frame)

    # corners, ids, rejected = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=aruco_params)
    
    if ids is not None:
        # Draw detected markers and IDs
        cv.aruco.drawDetectedMarkers(frame, corners, ids)
    
    # Display the result
    cv.imshow('ArUco Marker Detection', frame)
    
    if cv.waitKey(1) & 0xFF == 27:  # Press Esc to exit
        break

# Release the camera and close OpenCV windows
cap.release()
cv.destroyAllWindows()
