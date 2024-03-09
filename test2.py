import cv2

# Open the default camera (0)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Check if the frame is captured correctly
    if not ret:
        print("Error: Could not capture frame.")
        break

    # Display the captured frame
    cv2.imshow("Frame", frame)

    # Check for key press
    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' to exit
        break
    elif key == ord('s'):  # Press 's' to save image
        filename = "captured_image.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")

# Release the camera
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
