import cv2

# Create a VideoCapture object
cap = cv2.VideoCapture(0)  # 0 represents the default webcam on your system

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Capture a frame
ret, frame = cap.read()

# Check if the frame is captured correctly
if not ret:
    print("Error: Could not capture frame.")
    cap.release()  # Release the VideoCapture object
    exit()

# Display the captured frame
cv2.imshow("Webcam", frame)
cv2.waitKey(0)  # Wait for any key press
cv2.destroyAllWindows()  # Close all OpenCV windows

# Release the VideoCapture object
cap.release()
