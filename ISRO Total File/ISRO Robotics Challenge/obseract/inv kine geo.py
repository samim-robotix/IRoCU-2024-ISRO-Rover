import math

def calculate_joint_angles(x, y, L1, L2, L3):
    # Calculate the position of the wrist (joint 2)
    r = math.sqrt(x**2 + y**2)  # distance from the base to the end effector
    if r > (L1 + L2 + L3):
        raise ValueError("The position is unreachable with the given arm lengths.")
    
    # Assume a fixed orientation angle phi for the end effector
    phi = math.atan2(y, x)
    
    # Solve for theta3 first
    cos_theta3 = (x**2 + y**2 - L1**2 - L2**2 - L3**2) / (2 * L2 * L3)
    if not -1 <= cos_theta3 <= 1:
        raise ValueError("cos_theta3 out of range, no valid solution.")
    
    theta3 = math.acos(cos_theta3)
    
    # Solve for theta2 using the Law of Cosines
    k1 = L1 + L2 * math.cos(theta3)
    k2 = L2 * math.sin(theta3)
    theta2 = math.atan2(y, x) - math.atan2(k2, k1)
    
    # Solve for theta1
    cos_theta1 = (x**2 + y**2 + L1**2 - L2**2 - L3**2) / (2 * L1 * math.sqrt(x**2 + y**2))
    if not -1 <= cos_theta1 <= 1:
        raise ValueError("cos_theta1 out of range, no valid solution.")
    
    theta1 = math.atan2(y, x) - math.atan2(math.sqrt(1 - cos_theta1**2), cos_theta1)
    
    return math.degrees(theta1), math.degrees(theta2), math.degrees(theta3)

# Example usage
x = 0.64  # x-coordinate of the end effector
y = 0.1  # y-coordinate of the end effector
L1 = 0.26  # length of the first segment
L2 = 0.24  # length of the second segment
L3 = 0.24  # length of the third segment

try:
    theta1, theta2, theta3 = calculate_joint_angles(x, y, L1, L2, L3)
    print(f"The angles are: theta1 = {theta1:.2f}, theta2 = {theta2:.2f}, theta3 = {theta3:.2f}")
except ValueError as e:
    print(e)
