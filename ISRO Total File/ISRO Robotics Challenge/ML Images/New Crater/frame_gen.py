import cv2
import os

# Define video path and output folder path
video_path = "WhatsApp Video 2024-06-04 at 06.38.08_81e3fd5d.mp4"
output_folder = "Extracted_Frames"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Capture the video
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error opening video!")
    exit()

# Get video frame rate (might not be accurate)
fps = cap.get(cv2.CAP_PROP_FPS)

# Calculate frame interval in milliseconds
frame_interval = int(1000 / fps)  # Convert fps to milliseconds

# Counter for frame number and starting time
frame_count = 186
start_time = 0.0

while True:
    # Read a frame
    ret, frame = cap.read()

    # Check if frame is read correctly
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

    # Calculate current time in seconds
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

    # Extract frame every 0.5 seconds
    if current_time - start_time >= 1.0:
        # Create filename with frame number
        filename = f"{output_folder}/frame_{frame_count}.jpg"

        # Save the frame
        cv2.imwrite(filename, frame)

        # Update frame count and starting time
        frame_count += 1
        start_time = current_time

    # Exit loop if reaching video end
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

print(f"Extracted {frame_count} frames and saved to {output_folder}")
