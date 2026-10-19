import cv2
import os

def extract_frames(video_path, output_folder, time_interval_sec):
  """
  Extracts frames from a video at a predefined time interval and saves them to a folder.

  Args:
      video_path (str): Path to the input video file.
      output_folder (str): Path to the folder where frames will be saved.
      time_interval_sec (float): Time interval in seconds between extracted frames.
  """

  # Create output folder if it doesn't exist
  os.makedirs(output_folder, exist_ok=True)

  # Open video capture object
  cap = cv2.VideoCapture(video_path)

  # Check if video opened successfully
  if not cap.isOpened():
    print("Error opening video:", video_path)
    return

  # Get video frame rate (may not be accurate, use for reference)
  frame_rate = cap.get(cv2.CAP_PROP_FPS)
  print("Video frame rate (may not be accurate):", frame_rate, "FPS")

  # Calculate frame skip count based on time interval
  frame_skip = int(frame_rate * time_interval_sec)

  # Initialize frame count
  frame_count = 0

  # Loop through video frames
  while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
      print("No more frames to read.")
      break

    # Skip frames based on time interval
    if frame_count % frame_skip == 0:
      # Generate frame filename with timestamp
      filename = os.path.join(output_folder, f"frame1_{frame_count}.jpg")
      print(f"Saving frame {frame_count} at {filename}")

      # Save the frame
      cv2.imwrite(filename, frame)

    # Increment frame count
    frame_count += 1

  # Release the video capture object
  cap.release()
  cv2.destroyAllWindows()

# Example usage
video_path = "new video/Vid1.mp4"
output_folder = "extracted_frames"
time_interval_sec = 0.3  # Extract frames every 0.5 seconds

extract_frames(video_path, output_folder, time_interval_sec)
print("Frames extracted successfully!")
