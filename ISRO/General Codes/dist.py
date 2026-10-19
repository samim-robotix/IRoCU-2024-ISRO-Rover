import math

def calculate_distance_and_angle(current_x, current_y, current_orientation, goal_x, goal_y, goal_orientation):
    # Calculate the distance
    distance = math.sqrt((goal_x - current_x) ** 2 + (goal_y - current_y) ** 2)
    
    # Calculate the angle to the goal
    angle_to_goal = math.atan2(goal_y - current_y, goal_x - current_x)
    
    # Convert current orientation and goal orientation from degrees to radians
    current_orientation_rad = math.radians(current_orientation)
    goal_orientation_rad = math.radians(goal_orientation)
    
    # Calculate the required rotation angle
    required_rotation = angle_to_goal - current_orientation_rad
    
    # Normalize the rotation angle to the range [-pi, pi]
    required_rotation = (required_rotation + math.pi) % (2 * math.pi) - math.pi
    
    # Calculate the final orientation
    #final_orientation = (goal_orientation_rad - angle_to_goal) % (2 * math.pi) - math.pi
    
    # Convert the final orientation back to degrees
    final_orientation_degrees = math.degrees(required_rotation)

    
    return distance, math.degrees(required_rotation), final_orientation_degrees

# Example usage:
current_x = 3
current_y = -2.3
current_orientation = 15  # in degrees

goal_x = 3.4
goal_y = -1.5
goal_orientation = 0  # in degrees

distance, rotation_angle, final_orientation = calculate_distance_and_angle(current_x, current_y, current_orientation, goal_x, goal_y, goal_orientation)

print(f"Distance: {distance}")
print(f"Rotation Angle: {rotation_angle} degrees")
print(f"Final Orientation: {final_orientation} degrees")
