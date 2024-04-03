import RPi.GPIO as GPIO
import time
import json

# GPIO pins
IN1 = 17  #  pin numbers based on your wiring
IN2 = 27  #  pin numbers based on your wiring
ENA = 22  #  pin numbers based on your wiring for PWM speed control
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Setup PWM
pwm = GPIO.PWM(ENA, 100)  # Set frequency to 100 Hz
pwm.start(0)  # Start PWM with 0% duty cycle

def control_motor(analog_ly_value):
    if analog_ly_value > 0:
        # actuator forward
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        pwm.ChangeDutyCycle(100)  # Set duty cycle to 100% for full speed
    elif analog_ly_value < 0:
        # actuator reverse
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        pwm.ChangeDutyCycle(100)  # Set duty cycle to 100% for full speed
    else:
        # Stop
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        pwm.ChangeDutyCycle(0)  # Set duty cycle to 0 to stop the motor

try:
    while True:
        # Replace 'variable_data.json' with the actual path to your JSON file if necessary
        data = read_json_file('variable_data.json')
        if data is not None:
            control_motor(data.get('Analog_LY', 0))
        time.sleep(0.1)  # Adjust as necessary 

finally:
    pwm.stop()  # Stop PWM
    GPIO.cleanup()  # Clean up GPIO
