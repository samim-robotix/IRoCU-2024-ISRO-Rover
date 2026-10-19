import smbus2
import time
import board
import busio
import adafruit_bno055

# Define I2C bus number based on your Jetson Nano Orin configuration
bus_number = 1  # Adjust if needed

# Create an I2C communication object
i2c = smbus2.SMBus(bus_number)

# Create an I2C communication object for the sensor
i2c_sensor = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c_sensor)

# Define I2C slave address of the Arduino
slave_address = 9  # Adjust based on your Arduino sketch

def send_instruction(instruction):
    """Sends an instruction to the Arduino slave."""
    try:
        i2c.write_byte(slave_address, instruction)
        print(f"Sent instruction: {instruction}")
        return 0
    except Exception as e:
        print(f"Error sending instruction: {e}")
        return 0

def wait_for_ack(timeout=2):
    """Waits for an acknowledgment byte from the Arduino with a timeout."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            ack = i2c.read_byte(slave_address)
            if ack == 1:
                print(f"Moving Forward: {ack}")
                return True
            elif ack == 2:
                print(f"Moving Backward: {ack}")
                return True
            elif ack == 3:
                print(f"Turning Left: {ack}")
                return True
            elif ack == 4:
                print(f"Turning Right: {ack}")
                return True
            elif ack == 5:
                print(f"Stopped: {ack}")
                return True
            elif ack == 6:
                print(f"Give heading: {ack}")
                return True
            else:
                print(f"Moving to: {ack} cm")
        except Exception as e:
            print(f"Error receiving ack: {e}")
        time.sleep(0.1)  # Adjust polling interval as needed
    print("Timeout waiting for acknowledgment")
    return False

def get_current_heading():
    """Retrieve the current heading from the BNO055 sensor."""
    heading = sensor.euler[0]
    if heading is None:
        return 0
    return heading

def turn_to_angle(target_angle):
    """Turn the rover to the target angle."""
    current_heading = get_current_heading()
    turn_right = (target_angle - current_heading) % 360
    turn_left = (current_heading - target_angle) % 360

    if turn_right <= turn_left:
        send_instruction(4)  # Assuming '4' is the instruction to start turning right
        while True:
            current_heading = get_current_heading()
            # print(f"Current Heading: {current_heading} degrees")
            if abs(current_heading - target_angle) < 1:
                break
            time.sleep(0.1)  # Adjust polling interval as needed
    else:
        send_instruction(3)  # Assuming '3' is the instruction to start turning left
        while True:
            current_heading = get_current_heading()
            # print(f"Current Heading: {current_heading} degrees")
            if abs(current_heading - target_angle) < 1:
                break
            time.sleep(0.1)  # Adjust polling interval as needed

    send_instruction(5)  # Assuming '5' is the instruction to stop

# Example usage
# while True:
#     instruction = int(input("Enter instruction for Arduino (or '0' to quit): "))
#     if instruction == 0:
#         break

#     send_instruction(instruction)  # Encode for byte transmission

#     if not wait_for_ack():
#         print("Failed to receive acknowledgment. Retrying...")
#         continue

#     if instruction == 6:
#         initial_heading = get_current_heading()
#         print(f"Initial Heading: {initial_heading} degrees")

#         # Input the target heading directly
#         target_angle = float(input("Enter the target heading: "))
#         if target_angle < 0 or target_angle >= 360:
#             print("Invalid target heading. Please enter a value between 0 and 359.")
#         else:
#             print(f"Target Heading: {target_angle} degrees")
#             turn_to_angle(target_angle)
            


# print("Communication closed")

