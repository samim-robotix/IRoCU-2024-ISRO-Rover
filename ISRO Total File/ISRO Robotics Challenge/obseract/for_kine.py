import numpy as np

def dh_transform_matrix(theta, d, a, alpha):
    """ Create the transformation matrix from DH parameters. """
    alpha = np.radians(alpha)  # Convert alpha to radians
    theta = np.radians(theta)  # Convert theta to radians
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha),  np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0,              np.sin(alpha),               np.cos(alpha),              d],
        [0,              0,                           0,                          1]
    ])

def forward_kinematics(thetas):
    # DH parameters
    d = [0.1, 0, 0, 0]
    a = [0, 0.26, 0.24, 0.24]
    alpha = [90, 0, 0, 0]

    # Compute individual transformation matrices
    T1 = dh_transform_matrix(thetas[0], d[0], a[0], alpha[0])
    T2 = dh_transform_matrix(thetas[1], d[1], a[1], alpha[1])
    T3 = dh_transform_matrix(thetas[2], d[2], a[2], alpha[2])
    T4 = dh_transform_matrix(thetas[3], d[3], a[3], alpha[3])

    # Combine the transformation matrices
    T = T1 @ T2 @ T3 @ T4

    # Extract end effector position
    position = T[:3, 3]

    # Filter and round off the position values
    position = np.where(np.abs(position) < 0.005, 0, position)
    position = np.round(position, 2)
    
    return position

# Example usage
thetas = [0  ,  60  , -60   , 15]  # Replace these values with the actual joint angles in degrees
position = forward_kinematics(thetas)
print(f"End effector position: {position}")

