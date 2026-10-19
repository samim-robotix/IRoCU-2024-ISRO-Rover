import cv2
import numpy as np

# Initialize global variables
color_lower = None
color_upper = None
selected_color = False

# Mouse callback function
def select_color(event, x, y, flags, param):
    global color_lower, color_upper, selected_color
    
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_color = True
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        selected_pixel = hsv_frame[y, x]
        
        # Set color range for masking
        color_lower = np.array([selected_pixel[0] - 10, 100, 100])
        color_upper = np.array([selected_pixel[0] + 10, 255, 255])

# Initialize video capture
cap = cv2.VideoCapture(0)

# Set up the mouse callback
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', select_color)

while True:
    # Read the current frame
    ret, frame = cap.read()
    if not ret:
        break
    
    if selected_color:
        # Convert the frame to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create a mask for the selected color
        mask = cv2.inRange(hsv_frame, color_lower, color_upper)
        
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 2500:
                # Draw bounding box around the object
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display the frame
    cv2.imshow('Frame', frame)
    
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
