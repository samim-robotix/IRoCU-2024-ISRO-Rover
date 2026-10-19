import math

def calculate_end_effector_position(theta1, theta2, theta3, L1, L2, L3):
    # Convert angles from degrees to radians
    theta1 = math.radians(theta1)
    theta2 = math.radians(theta2)
    theta3 = math.radians(theta3)
    
    # Calculate the position of the first joint
    x1 = L1 * math.cos(theta1)
    y1 = L1 * math.sin(theta1)
    
    # Calculate the position of the second joint
    x2 = x1 + L2 * math.cos(theta1 + theta2)
    y2 = y1 + L2 * math.sin(theta1 + theta2)
    
    # Calculate the position of the end effector
    x = x2 + L3 * math.cos(theta1 + theta2 + theta3)
    y = y2 + L3 * math.sin(theta1 + theta2 + theta3)
    
    return x, y

# Example usage
theta1 = 30  # angle in degrees
theta2 = -60  # angle in degrees
theta3 = 60  # angle in degrees
L1 = 0.26      # length in units
L2 = 0.24      # length in units
L3 = 0.24      # length in units

x, y = calculate_end_effector_position(theta1, theta2, theta3, L1, L2, L3)
print(f"The position of the end effector is: ({x:.2f}, {y:.2f})")
