import numpy as np
import csv
import time

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

def generate_combinations_and_save_to_csv():
    # Define the joint angle ranges
    j1_range = range(0, 181, 5)  # J1 from 0 to 180 degrees
    j2_range = range(0, 121, 5)  # J2 from 0 to 120 degrees
    j3_range = range(-90, -29, 5)  # J3 from -90 to 0 degrees
    j4_range = range(-90, -79, 1)  # J4 from -90 to 0 degrees

    # Open a CSV file to save the results
    with open('robotic_arm_positions_normal03.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['J1', 'J2', 'J3', 'J4', 'X', 'Y', 'Z'])

        # Iterate over all combinations of joint angles
        for j1 in j1_range:
            for j2 in j2_range:
                for j3 in j3_range:
                    for j4 in j4_range:
                        thetas = [j1, j2, j3, j4]
                        position = forward_kinematics(thetas)

                        # Filter out positions where X or Y is less than 0.1
                        
                        writer.writerow([j1, j2, j3, j4] + position.tolist())

# Measure the time required to run the script
start_time = time.time()

# Run the function to generate the combinations and save to CSV
generate_combinations_and_save_to_csv()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time required: {elapsed_time:.2f} seconds")
