import serial
import keyboard
import time

serial_port = "COM6"
baud_rate = 9600

ser = serial.Serial(serial_port, baud_rate)

# Define debounce interval in seconds
debounce_interval = 0.01  # Adjust as needed

# Initialize last input time
last_input_time = time.time()

try:
    while True:
        line = ser.readline().decode('utf-8').strip()

        # Check if debounce interval has passed since last input
        if time.time() - last_input_time < debounce_interval:
            continue

        print("Arduino says:", line)
        if line == "a0":
            keyboard.press_and_release('up')
        elif line == "a2":
            keyboard.press_and_release('left')
        elif line == "a1":
            keyboard.press_and_release('down')
        elif line == "a3":
            keyboard.press_and_release('right')
        
        # Update last input time
        last_input_time = time.time()
        
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
