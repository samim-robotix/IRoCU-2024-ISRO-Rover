import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_architecture_diagram(output_path):
    fig, ax = plt.subplots(figsize=(26, 14.5), facecolor='#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Main Diagram Title Block
    title_box = patches.FancyBboxPatch((0.04, 0.915), 0.92, 0.068, boxstyle='round,pad=0.008,rounding_size=0.015',
                                       facecolor='#111827', edgecolor='#00F0FF', linewidth=2.0, zorder=3)
    ax.add_patch(title_box)
    ax.text(0.50, 0.954, "PROJECT OBSERACT — HARDWARE & EMBEDDED SYSTEM ARCHITECTURE",
            color='#00F0FF', fontsize=20, weight='bold', ha='center', va='center', zorder=5)
    ax.text(0.50, 0.928, "ISRO Robotics Challenge (URSC 2024) | 5th Position Nationally | Team OBSERACT — Jadavpur University",
            color='#94A3B8', fontsize=12, weight='bold', ha='center', va='center', zorder=5)

    def draw_node(x, y, w, h, title, subtitle, items, border='#38BDF8', header_bg='#1E293B', title_c='#00F0FF', bg='#111827'):
        # shadow
        ax.add_patch(patches.FancyBboxPatch((x+0.003, y-0.003), w, h, boxstyle='round,pad=0.005,rounding_size=0.012',
                                            facecolor='#030712', edgecolor='none', alpha=0.6, zorder=2))
        # body
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.005,rounding_size=0.012',
                                            facecolor=bg, edgecolor=border, linewidth=1.8, zorder=3))
        # header
        hh = 0.038
        ax.add_patch(patches.FancyBboxPatch((x, y+h-hh), w, hh, boxstyle='round,pad=0.005,rounding_size=0.012',
                                            facecolor=header_bg, edgecolor=border, linewidth=1.2, zorder=4))
        ax.text(x+w/2, y+h-hh/2, title, color=title_c, fontsize=11, weight='bold', ha='center', va='center', zorder=5)
        cy = y + h - hh - 0.026
        if subtitle:
            ax.text(x+0.018, cy, subtitle, color='#38BDF8', fontsize=8.8, style='italic', weight='bold', ha='left', va='center', zorder=5)
            cy -= 0.026
        for item in items:
            ax.text(x+0.018, cy, f"• {item}", color='#E2E8F0', fontsize=8.3, ha='left', va='center', zorder=5)
            cy -= 0.022

    def draw_signal(x1, y1, x2, y2, label="", color='#00F0FF', lw=2.2, rad=0.0, style='-|>', label_bg='#0F172A'):
        arrow = patches.FancyArrowPatch((x1, y1), (x2, y2),
                                        connectionstyle=f"arc3,rad={rad}",
                                        arrowstyle=style,
                                        mutation_scale=16,
                                        color=color,
                                        linewidth=lw,
                                        zorder=6)
        ax.add_patch(arrow)
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            if rad != 0.0:
                my += rad * 0.15
            lbl_w = 0.085
            lbl_box = patches.FancyBboxPatch((mx - lbl_w/2, my - 0.012), lbl_w, 0.024,
                                             boxstyle='round,pad=0.004,rounding_size=0.008',
                                             facecolor=label_bg, edgecolor=color, linewidth=1.2, zorder=7)
            ax.add_patch(lbl_box)
            ax.text(mx, my, label, color=color, fontsize=7.5, weight='bold', ha='center', va='center', zorder=8)

    # ----------------- COLUMN 1: PERCEPTION & SENSORS -----------------
    draw_node(0.04, 0.705, 0.22, 0.185, "ARDUCAM 3D ToF SENSOR", "Time-of-Flight Spatial Perception",
              ["Interface: MIPI-CSI 2-lane port", "Measurement Range: 0.2m - 4.0m", "Depth Buffer Output: 16-bit raw", "Jet Colormap Spatial Visualization", "Obstacle Bearing & Distance Map"],
              border='#818CF8', title_c='#C7D2FE')

    draw_node(0.04, 0.500, 0.22, 0.185, "HD OPTICAL CAMERA", "Visual Tracking & Regolith Survey",
              ["Interface: USB 3.0 / CSI Stream", "Resolution: 1080p @ 30 FPS", "Low-Latency Video Capture", "LabelMe Crater Dataset Ingestion", "Ground Control Station Video Feed"],
              border='#818CF8', title_c='#C7D2FE')

    draw_node(0.04, 0.295, 0.22, 0.185, "ADAFRUIT BNO055 9-DOF IMU", "Absolute Orientation Sensor",
              ["Interface: I2C Bus 1 (3.3V Logic)", "Internal Fusion: Euler Angles (Heading)", "Angular Velocity & Linear Accel", "Dynamic Tilt on 15° Inclines", "Closed-Loop Heading PID ±1°"],
              border='#38BDF8', title_c='#BAE6FD')

    draw_node(0.04, 0.090, 0.22, 0.185, "END-EFFECTOR SENSORS", "Manipulator Gripper Telemetry",
              ["Piezoresistive FSR (Analog 0-1023)", "ADC Force Mapping: 0% - 100%", "Dual Microswitch Limit Stops", "Anti-Crush Grip Thresholding", "Sample Seating Verification"],
              border='#34D399', title_c='#A7F3D0')

    # ----------------- COLUMN 2: HIGH-LEVEL EDGE AI BRAIN -----------------
    draw_node(0.32, 0.500, 0.36, 0.390, "NVIDIA JETSON EDGE AI COMPUTING SYSTEM", "Jetson Orin / Nano Dev Kit — Linux / JetPack",
              ["Ultralytics YOLOv8 Crater Neural Model (20cm & 40cm, 98% Acc)",
               "Competition Obstacle Inference: OB150, OB300, SAMPLE & CONTAINER",
               "Arducam ToF 3D Point Cloud Clustering & Euclidean Distance Estimation",
               "Vector Field Obstacle Avoidance & Target Angle Heading Arbiter",
               "Analytical 5-DOF Denavit-Hartenberg (D-H) Inverse Kinematics Engine",
               "TCP/IP Video Socket Streaming Server (pickle + struct length encoding)",
               "I2C Master Arbitration Controller commanding MCU Slave @ Addr 0x09"],
              border='#00F0FF', header_bg='#083344', title_c='#00F0FF', bg='#0F172A')

    # ----------------- COLUMN 2 (BOTTOM): LOW-LEVEL EMBEDDED CONTROLLER -----------------
    draw_node(0.32, 0.090, 0.36, 0.355, "STM32F407VET6 ARM CORTEX-M4 MCU", "Low-Level Real-Time Deterministic Commutation Core (168 MHz)",
              ["Firmware: C++ / PlatformIO / STM32CubeIDE Bare-Metal Stack",
               "I2C Slave Node (Address: 0x09) — Command Packet Interpreter",
               "High-Speed SPI Interface (PA15 CS, PB3-PB5) to MCP2515 CAN Bus",
               "6x High-Torque Bipolar Stepper Driver PWM Channels with Current Limiting",
               "Closed-Loop Joint Actuation (Base, Shoulder, Elbow, Gripper Servos)",
               "FSR Analog ADC Reading & Joint Mechanical Limit Interrupt Lines",
               "Hardware Emergency Kill-Switch Interlock Signal Monitoring"],
              border='#F59E0B', header_bg='#451A03', title_c='#FBBF24', bg='#0F172A')

    # ----------------- INTER-TIER BRIDGE (JETSON <-> STM32) -----------------
    bridge_box = patches.FancyBboxPatch((0.40, 0.452), 0.20, 0.038, boxstyle='round,pad=0.005,rounding_size=0.01',
                                        facecolor='#03234B', edgecolor='#00F0FF', linewidth=1.5, zorder=6)
    ax.add_patch(bridge_box)
    ax.text(0.50, 0.471, "I2C BUS @ ADDR 0x09  (3.3V)", color='#00F0FF', fontsize=9, weight='bold', ha='center', va='center', zorder=7)
    # double arrow
    ax.add_patch(patches.FancyArrowPatch((0.50, 0.500), (0.50, 0.490), arrowstyle='<|-|>', mutation_scale=14, color='#00F0FF', linewidth=2.5, zorder=8))
    ax.add_patch(patches.FancyArrowPatch((0.50, 0.452), (0.50, 0.445), arrowstyle='<|-|>', mutation_scale=14, color='#00F0FF', linewidth=2.5, zorder=8))

    # ----------------- COLUMN 3 (TOP): GROUND TELEMETRY -----------------
    draw_node(0.74, 0.705, 0.22, 0.185, "5 GHz TELEMETRY & RF LINK", "Long-Range Ground Station Link",
              ["Ubiquiti LiteBeam LBE-M5-23", "Gain: 23 dBi High-Gain Directional", "Power over Ethernet (PoE) Driven", "Low-Latency Socket Protocol", "40-Minute Beyond-LOS Window"],
              border='#F43F5E', title_c='#FECDD3')

    # ----------------- COLUMN 3 (UPPER-MID): CAN BUS BACKBONE -----------------
    draw_node(0.74, 0.500, 0.22, 0.185, "MICROCHIP MCP2515 CAN NODE", "Automotive CAN 2.0B Communication",
              ["Baud Rate: 500 Kbps Noise-Immune", "TJA1050 High-Speed CAN Transceiver", "SPI-to-CAN Protocol Bridge", "Distributed Motor Driver Telemetry", "Thermal & Overload Status Broadcast"],
              border='#F59E0B', title_c='#FDE68A')

    # ----------------- COLUMN 3 (LOWER-MID): PHYSICAL ACTUATION -----------------
    draw_node(0.74, 0.295, 0.22, 0.185, "6-WHEEL ROCKER-BOGIE DRIVE", "Planetary Stepper Locomotion",
              ["6x 24V 54 kg-cm Bipolar Steppers", "Zero-Radius Differential Steering", "Regolith Hard-Nylon Tread Wheels", "15° Slope Climb (1 - 5 cm/s)", "Traverse 150mm/300mm Obstacles"],
              border='#10B981', title_c='#A7F3D0')

    # ----------------- COLUMN 3 (BOTTOM): MANIPULATOR -----------------
    draw_node(0.74, 0.090, 0.22, 0.185, "5-DOF MANIPULATOR ARM", "TRRT Kinematic Architecture",
              ["L1: 228.39mm, L2: 248.00mm Links", "Base, Shoulder, Elbow Geared Steppers", "Digital Precision Gripper Servos", "Closed-Loop Force Control (FSR)", "Autonomous Sample Drop Container"],
              border='#10B981', title_c='#A7F3D0')

    # ----------------- SIGNALS & BUS ROUTING -----------------
    # Sensors -> Jetson
    draw_signal(0.26, 0.795, 0.32, 0.795, label="MIPI-CSI", color='#818CF8')
    draw_signal(0.26, 0.590, 0.32, 0.650, label="USB 3.0", color='#818CF8')
    draw_signal(0.26, 0.385, 0.32, 0.540, label="I2C BUS 1", color='#38BDF8')

    # Sensors -> STM32
    draw_signal(0.26, 0.180, 0.32, 0.180, label="ADC / GPIO", color='#34D399')

    # Jetson -> RF Antenna (Direct horizontal)
    draw_signal(0.68, 0.795, 0.74, 0.795, label="TCP SOCKET", color='#F43F5E', lw=2.5)

    # STM32 -> CAN MCP2515 (Clean upward diagonal)
    draw_signal(0.68, 0.380, 0.74, 0.560, label="SPI PA15 CS", color='#F59E0B', lw=2.2)

    # STM32 -> Rocker Bogie (Direct horizontal)
    draw_signal(0.68, 0.260, 0.74, 0.360, label="STEP / DIR PWM", color='#10B981', lw=2.5)

    # STM32 -> 5-DOF Arm (Direct horizontal)
    draw_signal(0.68, 0.150, 0.74, 0.150, label="JOINT PWM / ADC", color='#10B981', lw=2.5)

    # Power & E-Stop Banner at Bottom
    power_box = patches.FancyBboxPatch((0.04, 0.018), 0.92, 0.054, boxstyle='round,pad=0.008,rounding_size=0.012',
                                       facecolor='#1E1B4B', edgecolor='#6366F1', linewidth=1.5, zorder=3)
    ax.add_patch(power_box)
    ax.text(0.50, 0.048, "POWER DISTRIBUTION: 24V High-Discharge Li-Ion Battery ➔ Custom PDB (Buck Regulators 24V to 12V / 5V / 3.3V) ➔ XT60 Bus",
            color='#E0E7FF', fontsize=10.5, weight='bold', ha='center', va='center', zorder=5)
    ax.text(0.50, 0.030, "[ EMERGENCY SAFETY SYSTEM ]: Hardwired Mechanical Latching Kill-Switch Isolates All 24V Drive Rails & Arm Power Within Milliseconds",
            color='#F43F5E', fontsize=9.5, weight='bold', ha='center', va='center', zorder=5)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Architecture diagram generated: {output_path}")

def create_pipeline_diagram(output_path):
    fig, ax = plt.subplots(figsize=(25, 13.5), facecolor='#0B0F19')
    ax.set_facecolor('#0B0F19')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Main Title
    title_box = patches.FancyBboxPatch((0.04, 0.915), 0.92, 0.068, boxstyle='round,pad=0.008,rounding_size=0.015',
                                       facecolor='#111827', edgecolor='#10B981', linewidth=2.0, zorder=3)
    ax.add_patch(title_box)
    ax.text(0.50, 0.954, "PROJECT OBSERACT — AUTONOMOUS PERCEPTION & CONTROL PIPELINE",
            color='#10B981', fontsize=20, weight='bold', ha='center', va='center', zorder=5)
    ax.text(0.50, 0.928, "Sequential Dataflow: Raw Sensing ➔ Edge Neural AI ➔ 3D Perception ➔ Trajectory Planning ➔ Actuation ➔ Telemetry",
            color='#94A3B8', fontsize=12, weight='bold', ha='center', va='center', zorder=5)

    stages = [
        {
            "num": "STAGE 01",
            "title": "SENSOR INGESTION",
            "sub": "Multi-Modal Hardware Capture",
            "items": [
                "HD Camera: 1080p RGB Frame Acquisition (30 FPS)",
                "Arducam ToF: 16-bit Raw Depth Buffer Matrix",
                "BNO055: Euler Orientation (Pitch, Roll, Heading)",
                "FSR Gripper: Analog Contact Force Measurement",
                "Encoder Feeds: Motor Step Pulse Verification"
            ],
            "border": "#38BDF8",
            "title_c": "#BAE6FD",
            "x": 0.04
        },
        {
            "num": "STAGE 02",
            "title": "EDGE AI PERCEPTION",
            "sub": "TensorRT Accelerated YOLOv8",
            "items": [
                "Crater Model: 20cm & 40cm Regolith Craters (98% Acc)",
                "Obstacle Model: OB150 & OB300 Cube Identification",
                "Sample Detector: Cylindrical Sample Tube Tracking",
                "Container Segmenter: Target Drop-Zone Bounding Box",
                "ToF Depth Colormapping: Real-Time Metric Distances"
            ],
            "border": "#818CF8",
            "title_c": "#C7D2FE",
            "x": 0.23
        },
        {
            "num": "STAGE 03",
            "title": "AUTONOMOUS NAVIGATION",
            "sub": "Real-Time Decision Engine",
            "items": [
                "Vector Field Histogram: Repulsive Obstacle Vectors",
                "Closed-Loop Heading: turn_to_angle(target) via IMU",
                "Crater Avoidance & Traversal Strategy Selector",
                "Sample Target Centering: Error delta_x, delta_y Locking",
                "Motion Primitives: FWD, REV, TURN_L, TURN_R, STOP"
            ],
            "border": "#00F0FF",
            "title_c": "#00F0FF",
            "x": 0.42
        },
        {
            "num": "STAGE 04",
            "title": "KINEMATICS & CONTROL",
            "sub": "Dual-Tier Compute Arbitration",
            "items": [
                "5-DOF D-H Analytical Inverse Kinematics Engine",
                "Joint Target Angles (th1, th2, th3, th4, th5) in C++",
                "I2C Master Packet Dispatch to STM32 @ Addr 0x09",
                "Closed-Loop Gripper Control with FSR Thresholding",
                "CAN Bus 2.0B Frame Dispatch via SPI MCP2515"
            ],
            "border": "#F59E0B",
            "title_c": "#FDE68A",
            "x": 0.61
        },
        {
            "num": "STAGE 05",
            "title": "ACTUATION & TELEMETRY",
            "sub": "Ground Station Feedback",
            "items": [
                "6x 24V Stepper Motor Drivers: Microstepping Control",
                "Rocker-Bogie Chassis: 15° Slope Climb & Obstacle Scale",
                "Pick & Place: Sample Securement into Cargo Bay",
                "5GHz Ubiquiti RF: Compressed Frame Socket Streaming",
                "GCS Telemetry HUD: Real-Time Orientation & Coordinates"
            ],
            "border": "#10B981",
            "title_c": "#A7F3D0",
            "x": 0.80
        }
    ]

    card_w = 0.165
    card_h = 0.62
    card_y = 0.20

    for idx, s in enumerate(stages):
        x = s["x"]
        ax.add_patch(patches.FancyBboxPatch((x+0.003, card_y-0.003), card_w, card_h,
                                            boxstyle='round,pad=0.008,rounding_size=0.015',
                                            facecolor='#030712', edgecolor='none', alpha=0.6, zorder=2))
        ax.add_patch(patches.FancyBboxPatch((x, card_y), card_w, card_h,
                                            boxstyle='round,pad=0.008,rounding_size=0.015',
                                            facecolor='#111827', edgecolor=s["border"], linewidth=2.0, zorder=3))
        badge = patches.FancyBboxPatch((x + 0.015, card_y + card_h - 0.045), card_w - 0.03, 0.032,
                                       boxstyle='round,pad=0.004,rounding_size=0.008',
                                       facecolor='#1E293B', edgecolor=s["border"], linewidth=1.2, zorder=4)
        ax.add_patch(badge)
        ax.text(x + card_w/2, card_y + card_h - 0.029, s["num"], color=s["border"], fontsize=9.5, weight='bold', ha='center', va='center', zorder=5)

        ax.text(x + card_w/2, card_y + card_h - 0.075, s["title"], color=s["title_c"], fontsize=12, weight='bold', ha='center', va='center', zorder=5)
        ax.text(x + card_w/2, card_y + card_h - 0.105, s["sub"], color='#94A3B8', fontsize=8.5, style='italic', weight='bold', ha='center', va='center', zorder=5)

        ax.plot([x + 0.015, x + card_w - 0.015], [card_y + card_h - 0.125, card_y + card_h - 0.125], color=s["border"], lw=1.2, alpha=0.6, zorder=5)

        cy = card_y + card_h - 0.160
        for item in s["items"]:
            ax.plot(x + 0.018, cy, marker='s', markersize=4, color=s["border"], zorder=5)
            ax.text(x + 0.026, cy, item, color='#E2E8F0', fontsize=8.5, ha='left', va='center', zorder=5)
            cy -= 0.088

        if idx < len(stages) - 1:
            arrow = patches.FancyArrowPatch((x + card_w + 0.002, card_y + card_h/2),
                                            (stages[idx+1]["x"] - 0.004, card_y + card_h/2),
                                            arrowstyle='-|>', mutation_scale=20,
                                            color='#00F0FF', linewidth=2.5, zorder=6)
            ax.add_patch(arrow)

    summary_box = patches.FancyBboxPatch((0.04, 0.05), 0.92, 0.09, boxstyle='round,pad=0.008,rounding_size=0.012',
                                         facecolor='#0F172A', edgecolor='#38BDF8', linewidth=1.5, zorder=3)
    ax.add_patch(summary_box)
    ax.text(0.50, 0.105, "END-TO-END AUTONOMY LOOP PERFORMANCE BENCHMARKS", color='#38BDF8', fontsize=12, weight='bold', ha='center', va='center', zorder=5)
    ax.text(0.50, 0.075, "Perception Latency: ~30 ms (TensorRT Jetson GPU)  |  I2C Master/Slave Roundtrip: < 5 ms  |  CAN Bus Commutation: 500 Kbps Deterministic",
            color='#E2E8F0', fontsize=10, weight='bold', ha='center', va='center', zorder=5)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Pipeline diagram generated: {output_path}")

if __name__ == '__main__':
    create_architecture_diagram('assets/architecture.png')
    create_pipeline_diagram('assets/pipeline.png')
