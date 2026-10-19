import sys
import cv2
import numpy as np
import ArducamDepthCamera as ac
import math
import threading

MAX_DISTANCE = 4

def process_frame(depth_buf: np.ndarray, amplitude_buf: np.ndarray) -> np.ndarray:
    depth_buf = np.nan_to_num(depth_buf)
    amplitude_buf[amplitude_buf <= 7] = 0
    amplitude_buf[amplitude_buf > 7] = 255
    depth_buf = (1 - (depth_buf / MAX_DISTANCE)) * 255
    depth_buf = np.clip(depth_buf, 0, 255)
    result_frame = depth_buf.astype(np.uint8) & amplitude_buf.astype(np.uint8)
    return result_frame

class UserRect():
    def __init__(self) -> None:
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

selectRect = UserRect()

def on_mouse(event, x, y, flags, param):
    global selectRect
    
    if event == cv2.EVENT_LBUTTONDOWN:
        pass
    elif event == cv2.EVENT_LBUTTONUP:
        selectRect.start_x = x - 4 if x - 4 > 0 else 0
        selectRect.start_y = y - 4 if y - 4 > 0 else 0
        selectRect.end_x = x + 4 if x + 4 < 240 else 240
        selectRect.end_y=  y + 4 if y + 4 < 180 else 180

def calculate_depth(x: int, y: int) -> float:
    return depth_buf[y, x]  # Depth value at the selected pixel coordinate

def calculate_angle(x: int, y: int, frame_width = 1280, frame_height = 720):
    angle_x = math.degrees(math.atan2(x - frame_width // 2, frame_width))
    angle_y = math.degrees(math.atan2(y - frame_height // 2, frame_height))
    return angle_x
# for streaming the video over socket.   
def stream_frame():
    return result_image

def camera_thread():
    global depth_buf
    global amplitude_buf
    global result_image

    cam = ac.ArducamCamera()
    if cam.open(ac.TOFConnect.CSI, 0) != 0:
        print("Initialization failed")
    if cam.start(ac.TOFOutput.DEPTH) != 0:
        print("Failed to start camera")
    cam.setControl(ac.TOFControl.RANG, MAX_DISTANCE)
    cv2.namedWindow("preview", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("preview", on_mouse)
    while True:
        frame = cam.requestFrame(200)
        if frame is not None:
            depth_buf = frame.getDepthData()
            amplitude_buf = frame.getAmplitudeData()
            cam.releaseFrame(frame)
            amplitude_buf *= (255 / 1024)
            amplitude_buf = np.clip(amplitude_buf, 0, 255)

            cv2.imshow("preview_amplitude", amplitude_buf.astype(np.uint8))
            # depth_value, angle_x, angle_y = calculate_depth_and_angle(depth_buf, 
            #                                                            selectRect.start_x + (selectRect.end_x - selectRect.start_x) // 2, 
            #                                                            selectRect.start_y + (selectRect.end_y - selectRect.start_y) // 2,
            #                                                            depth_buf.shape[1],
            #                                                            depth_buf.shape[0])
            # print("Depth at selected pixel:", depth_value)
            # print("Angle from center in X:", angle_x)
            # print("Angle from center in Y:", angle_y)

            result_image = process_frame(depth_buf, amplitude_buf)
            result_image = cv2.applyColorMap(result_image, cv2.COLORMAP_JET)
            cv2.rectangle(result_image, (selectRect.start_x, selectRect.start_y), 
                                      (selectRect.end_x, selectRect.end_y), (128, 128, 128), 1)

            cv2.imshow("preview", result_image)

            key = cv2.waitKey(1)
            if key == ord("q"):
                cam.stop()
                cam.close()
                sys.exit(0)

def start_depth():
    camera_thread = threading.Thread(target=camera_thread)
    camera_thread.start()


