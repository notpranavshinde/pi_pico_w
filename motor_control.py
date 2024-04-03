import json
import time
import serial

# Function for mapping the Y values from -1 to 1, to 0 to 127 for left motor, and 128 to 255 for the right motor.
def map_y_to_motor_speed(y_value):
    left_motor_speed = int((y_value + 1) * 63.5)  # Scale -1 to 1 to 0 to 127
    right_motor_speed = left_motor_speed + 128  # Offset for right motor speed
    return left_motor_speed, right_motor_speed

# Function for calculating the differential for the X values and apply it to the motors' speeds.
def apply_differential_steering(x_value, left_motor_speed, right_motor_speed):
    if x_value != 0:  # Only apply differential steering if there is a turn (x is not 0).
        percentage = abs(x_value)  # Convert -1 to 1 range into 0 to 1.
        if x_value < 0:  # Turning left
            left_motor_speed = int(left_motor_speed * (1 - percentage))
        else:  # Turning right
            right_motor_speed = int(right_motor_speed * (1 - percentage))
    return left_motor_speed, right_motor_speed

while(True):
    # Loading the joystick values from the JSON file.
    try:
        with open('variable_data.json', 'r') as file:
            data = json.load(file)
            if data is None:
                raise ValueError("No data found in JSON file.")
            
            joystick_x = data.get('Analog_RX', 0)  # Use get method to provide a default value of 0
            joystick_y = data.get('Analog_RY', 0)  # Use get method to provide a default value of 0
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"There was an error reading the joystick values: {e}")
        joystick_x = 0
        joystick_y = 0

    # Map the joystick Y values to motor speeds.
    left_motor_speed, right_motor_speed = map_y_to_motor_speed(joystick_y)

    # Apply differential steering based on the joystick X values.
    left_motor_speed, right_motor_speed = apply_differential_steering(joystick_x, left_motor_speed, right_motor_speed)
    
    # Output the calculated speeds for debugging.
    print("______________________________________________________________________________________________________")
    print(f"Left motor speed: {left_motor_speed}")
    print(f"Right motor speed: {right_motor_speed}")
    print("______________________________________________________________________________________________________")

    # Code to actually set the motor speeds on the Raspberry Pi using GPIO or another method would go here.
    try:
        Sabretooth_Serial = serial.Serial('/dev/ttyS0', 9600)  # Defines serial port and baud rate
        print('Serial Port Connected')
        
        # Converts values into bytes and sends the data through the serial connection
        speed_data = bytes([left_motor_speed, right_motor_speed])  
        Sabretooth_Serial.write(speed_data)  
        
        # Uncomment the next line to adjust the communication or action interval
        # time.sleep(0.25)  # Adjust the sleep duration as needed
        
        # Uncomment the next lines to close the serial port after each transmission, if needed
        # Sabretooth_Serial.close()  # Close the serial port connection
        # print('Serial Port Disconnected')
        
    except serial.SerialException as e:  # Will happen if the serial port doesn't open
        print("Error: Could not open serial port.")
        print(e)

    time.sleep(0.01)  # Main loop sleep time
