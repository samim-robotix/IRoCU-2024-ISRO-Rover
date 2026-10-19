import cv2
import numpy as np

def get_average_hsv(frame, click_pos):


  # Get coordinates of the clicked pixel and its neighbors
  x, y = click_pos
  h, w, _ = frame.shape
  neighbor_coords = [(x_offset, y_offset) for x_offset in range(-1, 2)
                     for y_offset in range(-1, 2)
                     if 0 <= x + x_offset < w and 0 <= y + y_offset < h]

  # Convert frame to HSV color space
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  # Extract and average HSV values of the neighborhood
  hsv_values = []
  for neighbor_x, neighbor_y in neighbor_coords:
    hsv_values.append(hsv[neighbor_y, neighbor_x])
  average_hsv = np.mean(hsv_values, axis=0)

  return average_hsv

def click_event(event, x, y, flags, param):
  """Mouse click event callback function."""
  if event == cv2.EVENT_LBUTTONDOWN:
    # Get the clicked pixel position
    click_pos = (x, y)

    # Capture the frame for processing
    ret, frame = cap.read()

    # Calculate and print average HSV of the neighborhood
    average_hsv = get_average_hsv(frame.copy(), click_pos)
    print(f"Average HSV of clicked pixel neighborhood: {average_hsv}")

    # Optional: Display the clicked pixel and its neighbors (uncomment if desired)
    # cv2.circle(frame, click_pos, 5, (0, 0, 255), -1)
    # for neighbor_x, neighbor_y in neighbor_coords:
    #   cv2.circle(frame, (neighbor_x, neighbor_y), 2, (255, 0, 0), -1)
    # cv2.imshow('Frame', frame)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Create a named window
cv2.namedWindow('Frame')

# Set mouse click callback function
cv2.setMouseCallback('Frame', click_event)

while True:
  # Capture frame
  ret, frame = cap.read()

  # Display the frame
  cv2.imshow('Frame', frame)

  # Exit on 'q' key press
  if cv2.waitKey(1) == ord('q'):
    break

# Release resources
cap.release()
cv2.destroyAllWindows()
