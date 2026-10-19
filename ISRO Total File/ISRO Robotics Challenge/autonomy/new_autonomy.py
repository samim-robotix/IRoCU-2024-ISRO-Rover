import threading
import time
from ultralytics import YOLO  # type: ignore
import cv2
import math
from heading_i2c import send_instruction
from enum import Enum

# Enum for Task States
class TaskState(Enum):
    IDLE = 0
    CONTAINER_TRACKING = 1
    SAMPLE_TRACKING = 2
    AUTONOMOUS_MODE = 3
    COMMANDED_MODE = 4

# Global variables
task_state = TaskState.IDLE
CT = False
ST = False
results_cont = []
results_detection = []

lock = threading.Lock()

# Start webcam
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# Load models
model_detection = YOLO("blockmodel.pt")
model_cont = YOLO("cont.pt")

# Object classes
classNames_cont = ["CONTAINER"]
classNames_detection = ["OB150", "OB300", "SAMPLE"]

def draw_results(img, results_detection, results_cont):
    for r in results_detection:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            confidence = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            cv2.putText(img, f"{classNames_detection[cls]} {confidence}", org, font, fontScale, color, thickness)

    for r in results_cont:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            confidence = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            cv2.putText(img, f"{classNames_cont[cls]} {confidence}", org, font, fontScale, color, thickness)

    return img

def process_frame(img):
    global results_detection
    global results_cont

    with lock:
        results_detection = model_detection(img, stream=True, conf=0.65)
        results_cont = model_cont(img, stream=True, conf=0.65)

    img_result = draw_results(img, results_detection, results_cont)
    return img_result

def autonomy():
    global task_state
    global CT
    global ST

    prev_inst = 5
    frame_x = 320
    frame_y = 240

    while True:
        with lock:
            if task_state == TaskState.AUTONOMOUS_MODE and not CT and not ST:
                if not CT:
                    print("Starting container tracking...")
                    for r in results_cont:
                        boxes = r.boxes
                        for box in boxes:
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            center_x, center_y = (x2 + x1) / 2, (y2 + y1) / 2
                            area = (x2 - x1) * (y2 - y1)
                            print(area)

                            if center_x > frame_x + 50:
                                if prev_inst != 4:
                                    send_instruction(4)
                                print("Right")
                                prev_inst = 4
                            elif center_x < frame_x - 50:
                                if prev_inst != 3:
                                    send_instruction(3)
                                print("Left")
                                prev_inst = 3
                            elif frame_x - 50 < center_x < frame_x + 50:
                                if prev_inst != 1:
                                    send_instruction(5)
                                    send_instruction(1)
                                print("Forward")
                                prev_inst = 1

                            if area > 42000:
                                send_instruction(5)
                                CT = True
                                print("Container tracking completed.")
                
                if task_state == TaskState.AUTONOMOUS_MODE and CT and not ST:
                    print("Starting sample finding...")
                    for r in results_detection:
                        boxes = r.boxes
                        for box in boxes:
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                            cls = int(box.cls[0])
                            class_name = classNames_detection[cls]

                            if class_name == "SAMPLE":
                                center_x, center_y = (x2 + x1) / 2, (y2 + y1) / 2
                                area = (x2 - x1) * (y2 - y1)
                                print(area)
                                print(center_x, center_y)

                                if center_x > frame_x + 20:
                                    if prev_inst != 4:
                                        send_instruction(4)
                                    print("Right")
                                    prev_inst = 4
                                elif center_x < frame_x - 20:
                                    if prev_inst != 3:
                                        send_instruction(3)
                                    print("Left")
                                    prev_inst = 3
                                elif frame_x - 20 < center_x < frame_x + 20:
                                    if prev_inst != 1:
                                        send_instruction(5)
                                        send_instruction(1)
                                    print("Forward")
                                    prev_inst = 1

                                if 38000 < area < 42000 and frame_x - 20 < center_x < frame_x + 20:
                                    send_instruction(5)
                                    ST = True
                                    print("Sample finding completed.")
                                    
                if CT and ST:
                    print("Autonomous mode completed.")
                    task_state = TaskState.IDLE
                    CT = False
                    ST = False

        time.sleep(1)

def webcam_thread():
    while True:
        success, img = cap.read()
        if not success:
            break

        img_result = process_frame(img)
        cv2.imshow('Webcam', img_result)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_detection():
    webcam_thr = threading.Thread(target=webcam_thread)
    auto_mode = threading.Thread(target=autonomy)
    
    webcam_thr.start()
    auto_mode.start()
    

if __name__ == "__main__":
    start_detection()
    time.sleep(5)
    while True:
        user_input = input("Enter a task (CM, AM, SM): ").strip().upper()
        with lock:
            if user_input == "CM":
                task_state = TaskState.COMMANDED_MODE
                print("Manual control mode enabled.")
            elif user_input == "AM":
                task_state = TaskState.AUTONOMOUS_MODE
                print("Autonomous mode enabled.")
            elif user_input == "SM":
                task_state = TaskState.IDLE
                print("Sample mode enabled.")
            else:
                print("Invalid input. Please enter CM, AM, or SM.")
