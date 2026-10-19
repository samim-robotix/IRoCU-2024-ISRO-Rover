import time
import math
import board
import busio
import adafruit_bno055

class Navigation:
    def __init__(self, initial_position=(0.6, -0.6, 0), initial_heading=0):
        self.i2c = busio.I2C(board.SCL_1, board.SDA_1)
        self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)
        self.position = list(initial_position)  # [x, y, z]
        self.heading = initial_heading          # Heading in degrees
        self.velocity = [0, 0, 0]               # Initial velocity [vx, vy, vz]
        self.last_time = time.time()
        self.sensor.mode = 0x09
        self.target_position = None
        self.target_orientation = None

    def update_position_orientation(self):
        """Updates the current position and orientation using the IMU sensor."""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        # Get the linear acceleration from the sensor
        acceleration = self.sensor.linear_acceleration  # [ax, ay, az]

        # Update velocity by integrating acceleration
        self.velocity[0] += acceleration[0] * dt
        self.velocity[1] += acceleration[1] * dt
        self.velocity[2] += acceleration[2] * dt

        # Update position by integrating velocity
        self.position[0] += self.velocity[0] * dt + 0.5 * acceleration[0] * dt**2
        self.position[1] += self.velocity[1] * dt + 0.5 * acceleration[1] * dt**2
        self.position[2] += self.velocity[2] * dt + 0.5 * acceleration[2] * dt**2

        # Update heading (orientation)
        self.heading = self.sensor.euler[0]

        print(f"Updated position: {self.position}")
        print(f"Updated heading: {self.heading} degrees")

    def set_target(self, x, y, z, orientation):
        """Sets the target position and orientation."""
        self.target_position = (x, y, z)
        self.target_orientation = orientation

    def calculate_movement_command(self):
        """Calculates the movement command to reach the target position and orientation."""
        if self.target_position is None or self.target_orientation is None:
            return None

        # Calculate the difference in position and orientation
        delta_x = self.target_position[0] - self.position[0]
        delta_y = self.target_position[1] - self.position[1]
        #target_heading = math.degrees(math.atan2(delta_y, delta_x))
        delta_heading = self.target_orientation - self.heading

        # Normalize the delta_heading to be within [-180, 180]
        delta_heading = (delta_heading + 180) % 360 - 180

        print(f"Delta heading: {delta_heading} degrees")

        if abs(delta_heading) < 10:
            return "Forward"
        elif delta_heading > 0:
            return "Right"
        else:
            return "Left"

# Example usage:
if __name__ == "__main__":
    nav = Navigation()
    nav.set_target(1.0, -1.0, 0, 90)  # Example target

    while True:
        nav.update_position_orientation()
        command = nav.calculate_movement_command()
        if command:
            print(f"Movement command: {command}")
            # Here you would send the command to the robot
        time.sleep(1)