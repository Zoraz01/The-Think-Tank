import serial
import time

# --- Setup Serial Connection ---
# The port name is usually '/dev/ttyACM0' for an Arduino Uno.
# If that doesn't work, it might be '/dev/ttyACM1' or '/dev/ttyUSB0'.
try:
    # Use a 'with' block to ensure the serial port is closed properly
    with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as arduino:
        print(f"Connected to Arduino on port {arduino.port}.")
        time.sleep(2) # Wait for the Arduino to reset after connection

        if arduino.isOpen():
            print("Arduino connection open. Reading data...")
            # Loop forever to read and print data
            while True:
                if arduino.in_waiting > 0:
                    line = arduino.readline().decode('utf-8').rstrip()
                    print(f"Received: {line}")

except serial.SerialException as e:
    print(f"Error: Could not connect to Arduino. {e}")
    print("Check if the Arduino is plugged in and if the port name ('/dev/ttyACM0') is correct.")
except KeyboardInterrupt:
    print("\nProgram terminated by user.")
