import math

def calculate_movement_command(current_position, current_heading, target_position, target_orientation):
    """
    Calculates the movement command to reach the target position and orientation.
    
    Parameters:
    - current_position: tuple (x, y, z) of the current position
    - current_heading: float, the current heading in degrees
    - target_position: tuple (x, y, z) of the target position
    - target_orientation: float, the target orientation in degrees
    
    Returns:
    - str: movement command ("Forward", "Backward", "Left", "Right")
    """
    # Calculate the difference in position and orientation
    delta_x = target_position[0] - current_position[0]
    delta_y = target_position[1] - current_position[1]
    delta_distance = math.sqrt(delta_x**2+delta_y**2)
    #target_heading = math.degrees(math.atan2(delta_y, delta_x))
    delta_heading = target_orientation - current_heading

    # Normalize the delta_heading to be within [-180, 180]
    delta_heading = (delta_heading + 180) % 360 - 180

    print(f"Delta heading: {delta_heading} degrees")

    print(f"Delta Distance: {delta_distance} mts")

    if abs(delta_heading) < 10:
        return "Forward"
    elif abs(delta_heading) > 170:
        return "Backward"
    elif delta_heading > 0:
        return "Left"
    else:
        return "Right"



# Example usage:
current_position = (0.8,-0.8,0)
current_heading = 0
target_position = (1, -0.8, 0 )
target_orientation = 0

command = calculate_movement_command(current_position, current_heading, target_position, target_orientation)
print(f"Movement command: {command}")
