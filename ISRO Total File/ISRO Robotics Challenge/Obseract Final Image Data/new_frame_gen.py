import cv2
import os

def click_event(event, x, y, flags, param):
  """Mouse click event callback function to capture frames."""
  global frame_count
  if event == cv2.EVENT_LBUTTONDOWN:
    # Capture the current frame
    frame = param

    # Increment frame count and generate filename with chronological order
    frame_count += 1
    filename = f"captured_frame_{frame_count:04d}.jpg"

    # Save the captured frame
    cv2.imwrite(filename, frame)
    print(f"Frame captured and saved as: {filename}")

# Initialize frame count
frame_count = 0

# Load the video file
video_path = "star 1.mp4"  # Replace with your video path
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
  print("Error opening video file!")
  exit()

# Create a named window for video display
cv2.namedWindow('Video')

# Set mouse click callback function
cv2.setMouseCallback('Video', click_event)

while True:
  # Read a frame from the video
  ret, frame = cap.read()

  if not ret:
    print("End of video reached.")
    break

  # Display the frame
  cv2.imshow('Video', frame)

  # Exit on 'q' key press
  if cv2.waitKey(1) == ord('q'):
    break

# Release resources
cap.release()
cv2.destroyAllWindows()
