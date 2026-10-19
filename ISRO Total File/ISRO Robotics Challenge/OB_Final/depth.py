import numpy as np
import cv2

def find_farthest_object_in_section(image_path):
  """
  Finds the section (left, center, right) with the farthest object in the lower half of a grayscale image and visualizes the result.

  Args:
    image_path: Path to the grayscale image.
  """

  # Load the image
  img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
  img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # Convert to BGR for color visualization

  # Divide the image into three equal parts
  height, width = img.shape
  width_third = width // 3

  left_half = img[:, :width_third]
  center_half = img[:, width_third:2 * width_third]
  right_half = img[:, 2 * width_third:]

  # Find the darkest pixel in the lower half of each section
  left_min_val = np.min(left_half[height // 2:, :])
  center_min_val = np.min(center_half[height // 2:, :])
  right_min_val = np.min(right_half[height // 2:, :])

  # Determine the section with the darkest pixel
  if left_min_val <= center_min_val and left_min_val <= right_min_val:
    cv2.rectangle(img_color, (0, height // 2), (width_third, height), (0, 255, 0), 2)  # Green rectangle for left
    section = "left"
  elif center_min_val <= left_min_val and center_min_val <= right_min_val:
    cv2.rectangle(img_color, (width_third, height // 2), (2 * width_third, height), (0, 255, 0), 2)  # Green rectangle for center
    section = "center"
  else:
    cv2.rectangle(img_color, (2 * width_third, height // 2), (width, height), (0, 255, 0), 2)  # Green rectangle for right
    section = "right"

  cv2.imshow("Image with Section", img_color)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  return section

# Example usage
image_path = "g3.jpg"  # Replace with your image path
section_with_farthest_object = find_farthest_object_in_section(image_path)
print("The farthest object is in the:", section_with_farthest_object, "section")
