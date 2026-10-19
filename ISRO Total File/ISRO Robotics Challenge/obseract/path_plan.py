import cv2
import numpy as np

# Global variables to store the selected color and movement direction
selected_color = None
movement_direction = "No Obstacle"

def select_color(event, x, y, flags, param):
    global selected_color
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_color = frame[y, x]
        print(f"Selected color: {selected_color}")

def determine_movement(contours):
    global movement_direction
    frame_center_x = frame.shape[1] // 2

    if not contours:
        movement_direction = "Move Straight"
        return

    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    obstacle_center_x = x + w // 2

    print(obstacle_center_x)

    if abs(obstacle_center_x - frame_center_x) < 50:  # Obstacle in the center
        movement_direction = "Move Left"
    elif obstacle_center_x < frame_center_x:  # Obstacle on the left
        movement_direction = "Move Right"
    else:  # Obstacle on the right
        movement_direction = "Move Left"

cap = cv2.VideoCapture(0)
cv2.namedWindow('Video Feed')
cv2.setMouseCallback('Video Feed', select_color)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if selected_color is not None:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        selected_hsv_color = cv2.cvtColor(np.uint8([[selected_color]]), cv2.COLOR_BGR2HSV)[0][0]
        lower_bound = np.array([selected_hsv_color[0] - 10, 100, 100])
        upper_bound = np.array([selected_hsv_color[0] + 10, 255, 255])
        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Determine the movement direction based on the detected obstacle
        determine_movement(contours)

        for contour in contours:
            if cv2.contourArea(contour) > 5000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the movement direction on the frame
    cv2.putText(frame, f"Direction: {movement_direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('Video Feed', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
