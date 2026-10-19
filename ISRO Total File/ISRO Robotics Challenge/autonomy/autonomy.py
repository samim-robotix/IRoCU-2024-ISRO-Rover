from ultralytics import YOLO # type: ignore
import cv2
import math
import threading
from heading_i2c import send_instruction
import time


# Start webcam
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# Load models
model_detection = YOLO("blockmodel.pt")
model_cont = YOLO("cont.pt")

# Object classes
classNames_cont = ["CONTAINER"]   # Instance segmentation labels
classNames_detection = ["OB150","OB300","SAMPLE"] # Object detection labels

results_cont = []
AM = True

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
    global img_result
    global results_detection
    global results_cont

    results_detection = model_detection(img, stream=True, conf=0.65)
    results_cont = model_cont(img, stream=True, conf=0.65)

    img_result = draw_results(img, results_detection, results_cont)
    return img_result
    
# for streaming the video over socket. 
def stream_frame():
    return img_result

#container tracking code
def track_cont():
    AM = True
    if AM:
        global results_cont
        prev_inst = 5
        STOP = False

        frame_x = 320
        frame_y = 240
        while True:

            for r in results_cont:
                boxes = r.boxes

                for box in boxes:
                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values
                    center_x,center_y = (x2+x1)/2,(y2+y1)/2
                    area = (x2-x1)*(y2-y1)
                    print(area)

                    #turn_to_angle(360-container_heading(center_x,center_y))

                    if (center_x>frame_x+50 and not STOP):
                        if not prev_inst == 4:
                            send_instruction(4)
                        print("Right")
                        prev_inst = 4
                    elif (center_x<frame_x-50 and not STOP):
                        if not prev_inst == 3:
                            send_instruction(3)
                        print("Left")
                        prev_inst = 3
                        
                    elif(frame_x-50 < center_x <frame_x+50 and not STOP):
                        if not prev_inst == 1:
                            send_instruction(5)
                            #time.sleep(1)
                            send_instruction(1)
                        print("Forward")
                        prev_inst = 1

                    if area>42000 and not STOP:
                        #send_instruction(20)
                        send_instruction(5)
                        STOP = True
                        AM = False
                        break

                
    

#Finding the sample and aligning
def find_samp():
    prev_inst = 5
    STOP = False

    frame_x = 320
    frame_y = 240
    while not STOP:

        for r in results_detection:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                cls = int(box.cls[0])
                class_name = classNames_detection[cls]

                if class_name == "SAMPLE":
                    center_x,center_y = (x2+x1)/2,(y2+y1)/2
                    area = (x2-x1)*(y2-y1)
                    print(area)
                    print(center_x,center_y )

                    # #turn_to_angle(360-container_heading(center_x,center_y))

                    if (center_x>frame_x+20 and not STOP):
                        if not prev_inst == 4:
                            send_instruction(4)
                        print("Right")
                        prev_inst = 4
                    elif (center_x<frame_x-20 and not STOP):
                        if not prev_inst == 3:
                            send_instruction(3)
                        print("Left")
                        prev_inst = 3
                        
                    elif(frame_x-20 < center_x <frame_x+20 and not STOP):
                        if not prev_inst == 1:
                            send_instruction(5)
                            #time.sleep(1)
                            send_instruction(1)
                        print("Forward")
                        prev_inst = 1

                    if ((38000<area<42000)) and not STOP and (frame_x-20 < center_x <frame_x+20):
                        #send_instruction(20)
                        send_instruction(5)
                        STOP = True

        

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
    cont_track = threading.Thread(target=track_cont)
    webcam_thr.start()
    cont_track.start() 

if __name__ == "__main__":
    start_detection()
    #time.sleep(5)
    #AM = True