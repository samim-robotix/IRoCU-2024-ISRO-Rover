import cv2
import numpy as np

# Function to track red color
def track_red_object():
    # Capture video from the default camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read the frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame from BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

         # Define the range of blue color in HSV
        lower_blue = np.array([100, 150, 50])
        upper_blue = np.array([140, 255, 255])

        # Create a mask for blue color
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Variable to store the largest contour
        largest_contour = None
        max_area = 1000  # Minimum area threshold

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour

        # Draw bounding box and display orientation and centroid if the largest contour is found
        if largest_contour is not None:
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Calculate the centroid
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0

            # Draw the centroid
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            # # Determine if the bounding box is vertical or horizontal
            # if h > w:
            #     orientation = "Vertical"
            # else:
            #     orientation = "Horizontal"

            # # Display the orientation and centroid
            # cv2.putText(frame, f"{orientation}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, f"Centroid: ({cx}, {cy})", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame with the bounding box
        cv2.imshow('Red Object Tracking', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start tracking
track_red_object()
