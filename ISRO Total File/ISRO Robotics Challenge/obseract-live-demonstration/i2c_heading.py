import smbus2 # type: ignore
import time
import board # type: ignore
import busio # type: ignore
import adafruit_bno055 # type: ignore
import math
from server import send_message, receive_data
from obj_detect import *
from depth_cam import *
from robo_kine import *

# Constants
BUS_NUMBER = 1
WHEEL_DRIVE_ADDRESS = 9
ARM_DRIVE_ADDRESS = 8
ACK_TIMEOUT = 2

# Instructions
MOVE_FORWARD = 1
MOVE_BACKWARD = 2
TURN_LEFT = 3
TURN_RIGHT = 4
STOP = 5
SET_HEADING = 6

# I2C Communication objects
i2c = smbus2.SMBus(BUS_NUMBER)
i2c_sensor = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c_sensor)

def check_i2c_communication(address):
    try:
        i2c.read_byte(address)
        print(f"I2C communication with address {address} is working.")
        return True
    except Exception as e:
        print(f"Error communicating with address {address}: {e}")
        return False

def send_instruction(address, instruction, data=None):
    try:
        # Write an instruction byte followed by a data byte
        if data is not None:
            i2c.write_byte_data(address, instruction, data)
        # Write only instrcution byte
        else:
            i2c.write_byte(address, instruction)
        print(f"Sent instruction {instruction} to address {address}")
    except Exception as e:
        print(f"Error sending instruction to address {address}: {e}")

# Receive acknowledgement from the stm32
def wait_for_ack(address, timeout=ACK_TIMEOUT):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            ack = i2c.read_byte(address)
            if ack:
                print(f"Received acknowledgment {ack} from address {address}")
                return ack
        except Exception as e:
            print(f"Error receiving acknowledgment from address {address}: {e}")
        time.sleep(0.1)
    print(f"Timeout waiting for acknowledgment from address {address}")
    return None

# Get the current heading of the rover
def get_current_heading():
    heading = sensor.euler[0]
    if heading is None:
        return 0
    return heading

# Turn the rover to the desired angle
def turn_to_angle(target_angle):
    current_heading = get_current_heading()
    turn_right = (target_angle - current_heading) % 360
    turn_left = (current_heading - target_angle) % 360

    if turn_right <= turn_left:
        send_instruction(WHEEL_DRIVE_ADDRESS, TURN_RIGHT)
        while abs(get_current_heading() - target_angle) > 1:
            print(f"Current Heading: {get_current_heading()} degrees")
            time.sleep(0.1)
    else:
        send_instruction(WHEEL_DRIVE_ADDRESS, TURN_LEFT)
        while abs(get_current_heading() - target_angle) > 1:
            print(f"Current Heading: {get_current_heading()} degrees")
            time.sleep(0.1)

    send_instruction(WHEEL_DRIVE_ADDRESS, STOP)

# Arm controls---- to be completed
def control_arm(servo_angles):
    if len(servo_angles) != 5:
        print("Error: Please provide 5 angles for the servos.")
        return

    for i, angle in enumerate(servo_angles):
        send_instruction(ARM_DRIVE_ADDRESS, i + 1, angle)
        wait_for_ack(ARM_DRIVE_ADDRESS)

# Calculate distance and heading based on given coordinates
def calculate_distance_and_heading(current_x, current_y, target_x, target_y):
    delta_x = target_x - current_x
    delta_y = target_y - current_y
    distance = math.sqrt(delta_x**2 + delta_y**2)
    heading = math.degrees(math.atan2(delta_y, delta_x)) % 360
    return distance, heading

# COMMANDED MODE: Moves rover to desired coordinate
def move_to_coordinate(current_x, current_y, target_x, target_y):
    distance, target_heading = calculate_distance_and_heading(current_x, current_y, target_x, target_y)
    print(f"Calculated distance: {distance}, target heading: {target_heading}")

    turn_to_angle(target_heading)
    send_instruction(WHEEL_DRIVE_ADDRESS, MOVE_FORWARD, int(distance))
    wait_for_ack(WHEEL_DRIVE_ADDRESS)

# Autonomous navigation: To be completed
def navigate_autonomously():
    print("Navigating autonomously using sensors...")
    # Implement your autonomous navigation logic here

def initialize_i2c():
    if not (check_i2c_communication(WHEEL_DRIVE_ADDRESS) and check_i2c_communication(ARM_DRIVE_ADDRESS)):
        print("I2C communication check failed. Exiting...")
        return False
    return True

#Commanded mode
def commanded_mode(client):
    current_x, current_y = 0, 0  # Starting position, replace with actual values
    while True:
        send_message(client, "R: Enter X coordinate: ")
        target_x = int(receive_data(client))
        if target_x == -1:
            return "SM"
        send_message(client, "R: Enter Y coordinate: ")
        target_y = int(receive_data(client))
        move_to_coordinate(current_x, current_y, target_x, target_y)
        current_x, current_y = target_x, target_y
##---------------------------------------------------------------------------------------------------
##---------------------------------------------------------------------------------------------------
def autonomous_mode(client):
    SAMPLE_PICK = False
    while True:
        if not SAMPLE_PICK:
            samp_pos = get_coordinates("SAMPLE")
            actual_x, actual_y, actual_z = calculate_depth(samp_pos[0],samp_pos[1])

            control_arm(inv_kine(actual_x, actual_y, actual_z))

            turn_to_angle(0)
            cont_pos =  get_coordinates("CONTAINER")
            cont_heading = container_heading(cont_pos[0],cont_pos[1])
            turn_to_angle(cont_heading)
            send_instruction(WHEEL_DRIVE_ADDRESS, MOVE_FORWARD)

            while(cont_dist>0.35):
                cont_pos =  get_coordinates("CONTAINER")
                cont_dist = calculate_depth(cont_pos[0],cont_pos[1])
                
            send_instruction(WHEEL_DRIVE_ADDRESS, STOP)
            cont_pos =  get_coordinates("CONTAINER")
            actual_x, actual_y, actual_z = calculate_depth(samp_pos[0],samp_pos[1])

            control_arm(inv_kine(actual_x, actual_y, actual_z))

            SAMPLE_PICK = True








    

