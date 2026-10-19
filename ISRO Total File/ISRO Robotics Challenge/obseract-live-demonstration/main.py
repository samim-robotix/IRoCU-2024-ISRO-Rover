from server import *
from i2c_heading import initialize_i2c, commanded_mode, autonomous_mode
from obj_detect import start_detection
from depth_cam import start_depth

mode = "SM"

modes = {
    "SM": "STANDBY",
    "CM": "COMMANDED",
    "AM": "AUTONOMOUS"
}

# if __name__ == "__main__":
#     client = server_init()
#     send_message(client, "-*-*-*-*-*-*-*-*-*-*-*-* Hello Team Obseract -*-*-*-*-*-*-*-*-*-*-*-*")
#     while True:
#         send_message(client, f"R:\nCURRENTLY IN {modes[mode]} MODE\nCM: COMMANDED MODE\nAM:AUTONOMOUS MODE\nSM: STANDBY MODE")
#         mode = receive_data(client)
#         if(mode == "CM"):
#             mode = commanded_mode(client)

if __name__ == "__main__":
    start_detection()
    start_depth()

    client = server_init()
    send_message(client,"-*-*-*-*-*-*-*-*-*-*-*-* Hello Team Obseract -*-*-*-*-*-*-*-*-*-*-*-*")
    while True:
        send_message(client = f"R:\nCURRENTLY IN {modes[mode]} MODE\nCM: COMMANDED MODE\nAM:AUTONOMOUS MODE\nSM: STANDBY MODE")
        mode = receive_data()
        if(mode == "CM"):
            mode = commanded_mode(client)
        elif(mode == "AM"):
            if autonomous_mode(client) == "Parked":
                mode = "SM"
        elif (mode == "SM"):
            pass
    