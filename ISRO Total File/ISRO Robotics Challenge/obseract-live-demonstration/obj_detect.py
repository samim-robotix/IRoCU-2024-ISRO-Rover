from ultralytics import YOLO
import cv2
import math
import threading

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Load models
model_detection = YOLO("best_detection.pt")
model_segmentation = YOLO("best_segmentation.pt")

# Object classes
classNames_segmentation = ["C20", "C40"]   # Instance segmentation labels
classNames_detection = ["OB150", "OB300","SAMPLE","CONTAINER"] # Object detection labels



def get_coordinates(label_name):
    coordinates = []
    label_index = classNames_detection.index(label_name)
    for r in results_detection:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            if cls == label_index:
                x1, y1, x2, y2 = box.xyxy[0]
                x_center = (x1 + x2) // 2
                y_center = (y1 + y2) // 2
                coordinates.append((x_center, y_center))
    return coordinates

def draw_results(img, results_detection, results_segmentation):
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

    for r in results_segmentation:
        masks = r.masks
        for mask in masks:
            color_mask = (0, 255, 0)
            mask_img = mask.to_image()
            contours, _ = cv2.findContours(mask_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(img, contours, -1, color_mask, 3)
            x, y, w, h = cv2.boundingRect(contours[0])
            cls = int(mask.cls[0])
            org = (x, y)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (0, 255, 0)
            thickness = 2
            cv2.putText(img, classNames_segmentation[cls], org, font, fontScale, color, thickness)
    return img

def process_frame(img):
    global img_result
    global results_detection
    results_detection = model_detection(img, stream=True, conf=0.65)
    results_segmentation = model_segmentation(img, stream=True, conf=0.65)

    img_result = draw_results(img, results_detection, results_segmentation)
    return img_result
    
# for streaming the video over socket. 
def stream_frame():
    return img_result


def container_heading(center_x, center_y, frame_width=1280, frame_height=720):
    # Calculate the center of the frame
    frame_center_x = frame_width // 2
    frame_center_y = frame_height // 2

    # Calculate the vector from the center of the frame to the object
    vector_x = center_x - frame_center_x
    vector_y = center_y - frame_center_y

    # Calculate the angle using arctangent (in radians)
    angle_rad = math.atan2(vector_y, vector_x)

    # Convert radians to degrees
    angle_deg = math.degrees(angle_rad)

    return angle_deg


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
    webcam_thread = threading.Thread(target=webcam_thread)
    webcam_thread.start()
