import cv2
import math
from ultralytics import YOLO

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load the model
model = YOLO("best35.pt")

# Object classes
classNames = ["C20", "C40"]

# Function to determine movement direction
def determine_movement(obstacles):
    frame_center_x = 640 // 2  # Frame width is 640
    movement_direction = "Move Straight"
    if not obstacles:
        return movement_direction

    # Assume largest obstacle for direction
    largest_obstacle = max(obstacles, key=lambda item: item[1])
    x1, y1, x2, y2 = largest_obstacle[0]
    obstacle_center_x = (x1 + x2) // 2

    if abs(obstacle_center_x - frame_center_x) < 50:  # Obstacle in the center
        movement_direction = "Move Left"
    elif obstacle_center_x < frame_center_x:  # Obstacle on the left
        movement_direction = "Move Right"
    else:  # Obstacle on the right
        movement_direction = "Move Left"

    return movement_direction

while True:
    success, img = cap.read()
    if not success:
        break
    
    results = model(img, stream=True, conf=0.65)

    obstacles = []

    # Coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100
            print("Confidence --->", confidence)

            # Class name
            cls = int(box.cls[0])
            class_name = classNames[cls]
            print("Class name -->", class_name)

            # Set color based on class
            if class_name == "C20":
                color = (0, 255, 0)  # Green for C20
            elif class_name == "C40":
                color = (0, 0, 255)  # Red for C40
                # Add obstacle to list for movement determination
                obstacles.append(((x1, y1, x2, y2), box.conf[0]))
            
            # Put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)

            # Object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            thickness = 2
            cv2.putText(img, class_name, org, font, fontScale, color, thickness)

    # Determine movement direction
    movement_direction = determine_movement(obstacles)

    # Display movement direction on the frame
    cv2.putText(img, f"Direction: {movement_direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Show the video feed
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
