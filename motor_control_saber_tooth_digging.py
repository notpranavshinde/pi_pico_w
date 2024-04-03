import json
import time
import serial

# Initialize serial connection to Sabertooth motor driver
ser = serial.Serial('/dev/ttyS0', 9600)  # Adjust '/dev/ttyS0' as necessary
print("Serial connection established.")

# Function to control motors based on "Y" and "A" values
def control_motors(y, a):
    if y == 1:
        ser.write(b'1')  # Command to rotate motors clockwise
        print("Rotating motors clockwise.")
    elif a == 1:
        ser.write(b'2')  # Command to rotate motors anti-clockwise
        print("Rotating motors anti-clockwise.")
    else:
        print("No valid command found. Y and A are not set to 1.")

# Main function
def main():
    json_file = 'variable_data.json'  # Path to your JSON file
    print("Starting motor control script.")

    while True:
        try:
            # Read JSON file
            with open(json_file, 'r') as file:
                data = json.load(file)
                print(f"Read data: Y={data['Y']}, A={data['A']}")
            
            # Control motors based on "Y" and "A" values
            control_motors(data["Y"], data["A"])
            
            # Wait a bit before reading the file again
            time.sleep(1)
        except FileNotFoundError:
            print(f"Error: {json_file} not found. Make sure the file exists.")
            time.sleep(1)
        except json.JSONDecodeError:
            print(f"Error: {json_file} contains invalid JSON.")
            time.sleep(1)
        except KeyError:
            print(f"Error: 'Y' or 'A' key not found in {json_file}.")
            time.sleep(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
