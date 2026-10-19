import cv2
import math
from ultralytics import YOLO
import smbus2
import time

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load the model
model = YOLO("obs_new_best.pt")

# Object classes
classNames = ["OB150", "OB300","SAMPLE"]

# I2C setup
bus_number = 1  # Adjust if needed
i2c = smbus2.SMBus(bus_number)
slave_address = 9  # Adjust based on your Arduino sketch

# Movement directions and their corresponding hex codes
direction_codes = {
    "Move Straight": 1,
    "Move Left": 3,
    "Move Right": 4,
    "No Obstacle": 0x00
}

# Initialize the previous direction
previous_direction = "No Obstacle"

def send_instruction(instruction):
    """Sends an instruction to the Arduino slave."""
    try:
        i2c.write_byte(slave_address, instruction)
        print(f"Sent instruction: {instruction}")
    except Exception as e:
        print(f"Error sending instruction: {e}")

def wait_for_ack(timeout=2):
    """Waits for an acknowledgment byte from the Arduino with a timeout."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            ack = i2c.read_byte(slave_address)
            if ack == 1:
                print(f"Moving Forward:{ack}")
                return True
            elif ack == 2:
                print(f"Moving Backward:{ack}")
                return True
            elif ack == 3:
                print(f"Turning Left:{ack}")
                return True
            elif ack == 4:
                print(f"Turning Right:{ack}")
                return True
            elif ack == 5:
                print(f"Stopped:{ack}")
                return True
            else:
                print(f"Unexpected ack byte: {ack}")
        except Exception as e:
            print(f"Error receiving ack: {e}")
        time.sleep(0.1)
    print("Timeout waiting for acknowledgment")
    return False

def determine_movement(obstacles):
    frame_center_x = 640 // 2  # Frame width is 640
    movement_direction = "Move Straight"
    if not obstacles:
        return movement_direction

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
            if class_name == "OB150":
                color = (0, 255, 0)  # Green for C20
            elif class_name == "OB300":
                color = (0, 0, 255)  # Red for C40
                obstacles.append(((x1, y1, x2, y2), box.conf[0]))
            elif class_name == "SAMPLE":
            	color = (255, 0, 255)
            
            # Draw bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)

            # Put class name on the image
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            thickness = 2
            cv2.putText(img, class_name, org, font, fontScale, color, thickness)

    # Determine movement direction
    movement_direction = determine_movement(obstacles)

    # Send I2C command if direction changes
    if movement_direction != previous_direction:
        instruction = direction_codes[movement_direction]
        send_instruction(instruction)
        if wait_for_ack():
            previous_direction = movement_direction

    # Display movement direction on the frame
    cv2.putText(img, f"Direction: {movement_direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Show the video feed
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

