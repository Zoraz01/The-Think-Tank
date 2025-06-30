import time
import serial
import threading
from pyPS4Controller.controller import Controller

# --- Global variables to hold the current speed for each motor ---
# We use globals here because the controller library updates them in a separate thread.
left_speed = 0
right_speed = 0

class MyController(Controller):
    """
    Custom controller class to handle PS4 inputs and translate them to motor speeds.
    """
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    # --- TANK DRIVE CONTROLS ---
    # Left stick up/down controls forward and backward speed for both tracks.
    # Right stick left/right controls turning on the spot.

    def on_L3_y_at_rest(self):
        """Called when the left stick is released."""
        global left_speed
        left_speed = 0

    def on_L3_up(self, value):
        """Called when the left stick is pushed up."""
        global left_speed
        # PS4 controller values are -32767 (top) to 0. We map this to 255 to 0.
        left_speed = self.map_value(value, -32767, 0, 255, 0)
        
    def on_L3_down(self, value):
        """Called when the left stick is pushed down."""
        global left_speed
        # PS4 controller values are 0 to 32767 (bottom). We map this to 0 to -255.
        left_speed = self.map_value(value, 0, 32767, 0, -255)

    def on_R3_x_at_rest(self):
        """Called when the right stick is released."""
        global right_speed
        right_speed = 0

    def on_R3_left(self, value):
        """Called when the right stick is pushed left."""
        global right_speed
        # Turning left should subtract from the right motor and add to the left
        right_speed = self.map_value(value, 0, -32767, 0, 255)
        
    def on_R3_right(self, value):
        """Called when the right stick is pushed right."""
        global right_speed
        # Turning right should add to the right motor and subtract from the left
        right_speed = self.map_value(value, 0, 32767, 0, -255)
        
    @staticmethod
    def map_value(x, in_min, in_max, out_min, out_max):
        """Helper function to map a value from one range to another."""
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def main():
    """
    Main function to connect to Arduino and send motor commands.
    """
    print("Looking for PS4 controller...")
    # Instantiate the controller.
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

    # *** THIS IS THE CORRECTED PART ***
    # Start the controller's listen() method in a separate thread
    controller_thread = threading.Thread(target=controller.listen)
    controller_thread.daemon = True  # Allows main program to exit even if thread is running
    controller_thread.start()
    
    print("Controller listener started. Looking for Arduino...")

    try:
        # Use a 'with' block for robust serial connection handling
        with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as arduino:
            print(f"Connected to Arduino on {arduino.port}. Ready for commands.")
            time.sleep(2) # Wait for Arduino to reset

            while True:
                # --- Mixing Logic ---
                # This combines the forward/backward speed with the turning speed.
                # Note: Right stick controls turning, so it affects both motors oppositely.
                final_left = left_speed - right_speed
                final_right = left_speed + right_speed

                # Constrain values to the -255 to 255 range
                final_left = max(min(final_left, 255), -255)
                final_right = max(min(final_right, 255), -255)

                # Format the command string that the Arduino understands
                command = f"M,{final_left},{final_right}\n"

                # Send the command to the Arduino
                arduino.write(command.encode('utf-8'))
                
                # Print for debugging
                print(f"Sending -> Left: {final_left}, Right: {final_right}")

                # Send commands roughly 20 times per second
                time.sleep(0.05)

    except serial.SerialException as e:
        print(f"Error: Could not connect to Arduino. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
