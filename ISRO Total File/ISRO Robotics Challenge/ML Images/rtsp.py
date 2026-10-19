import cv2

def display_rtsp_feed(rtsp_url):
    """Displays an RTSP video feed using OpenCV."""

    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error opening video stream or file")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break

        # Display the frame using OpenCV
        cv2.imshow('RTSP Video Stream', frame)

        # Handle user input for termination (e.g., 'q' or 'Esc' key)
        if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == 27:
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

# Example usage (replace with a valid RTSP URL)
rtsp_url = "rtsp://192.168.1.102:8080/"
display_rtsp_feed(rtsp_url)
