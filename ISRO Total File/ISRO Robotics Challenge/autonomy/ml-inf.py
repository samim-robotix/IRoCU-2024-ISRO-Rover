from ultralytics import YOLO
import cv2
import math 
import time
from heading_i2c import send_instruction, turn_to_angle

# start webcam
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

frame_x = 320
frame_y = 240
# model
model = YOLO("samp.pt")
#model = YOLO("OBS_LASTone.pt")

prev_inst = 5

STOP = False
# object classes
#classNames = ["OB150","OB300","SAMPLE","CONTAINER"]
#classNames = ["C20","C40"]
classNames = ["CONTAINER"]



while True:
    success, img = cap.read()
    results = model(img, stream=True, conf=0.7)

    # coordinates
    for r in results:
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





            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            
            print(center_x,center_y )

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
            #cv2.putText(img, center, [center_x,center_y], font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

