import RPi.GPIO as GPIO
import time
import requests

# GPIO setup
LDR_PIN = 18  # GPIO pin for LDR
LED_PIN = 23  # GPIO pin for LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def measure_light():
    count = 0
    # Discharge capacitor
    GPIO.setup(LDR_PIN, GPIO.OUT)
    GPIO.output(LDR_PIN, GPIO.LOW)
    time.sleep(0.1)
    # Set as input and measure charge time
    GPIO.setup(LDR_PIN, GPIO.IN)
    while GPIO.input(LDR_PIN) == GPIO.LOW:
        count += 1
    return count

# ThingSpeak configuration
THINGSPEAK_WRITE_API_KEY = "YOUR_THINGSPEAK_WRITE_API_KEY"
UPDATE_URL = "https://api.thingspeak.com/update"

def send_to_thingspeak(light_level, led_state):
    data = {
        "api_key": THINGSPEAK_WRITE_API_KEY,
        "field1": light_level,
        "field2": led_state
    }
    response = requests.post(UPDATE_URL, data=data)
    if response.status_code == 200:
        print("Data sent to ThingSpeak!")
    else:
        print(f"Failed to send data: {response.status_code}")

try:
    while True:
        # Measure light level
        light_level = measure_light()
        print(f"Light Level: {light_level}")

        # Control LED based on light level (example logic)
        # Turn LED on if light level is below a certain threshold
        if light_level < 500:
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
            led_state = 1
            print("LED turned ON")
        else:
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn off LED
            led_state = 0
            print("LED turned OFF")

        # Send data to ThingSpeak
        send_to_thingspeak(light_level, led_state)

        # Wait 15 seconds (ThingSpeak rate limit)
        time.sleep(15)

except KeyboardInterrupt:
    print("Exiting program.")
finally:
    GPIO.cleanup()
