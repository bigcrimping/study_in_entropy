import network
import secrets
from utime import sleep
from machine import Pin
import urequests
import neopixel

NUM_LEDS = 42

# Function to fetch the latest reading from the NIST Randomness Beacon
def fetch_nist_randomness_beacon(retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = urequests.get('https://beacon.nist.gov/beacon/2.0/pulse/last')
            if response.status_code == 200:
                beacon_data = response.json()
                return beacon_data['pulse']['outputValue']
            else:
                print(f'Failed to fetch NIST Randomness Beacon, status code: {response.status_code}')
        except Exception as e:
            print(f'Exception while fetching NIST Randomness Beacon (attempt {attempt+1}/{retries}): {e}')
        sleep(delay)
    return None

# Function to update the WS2812B LEDs with a specific color
def set_leds_color(np, color):
    for i in range(NUM_LEDS):
        np[i] = color
    np.write()

def hex_to_rgb_scale(hex):
    return int(int(hex, 16) * (255/16))

# Function to cascade LED values to their positions.
# The final two beacon_values [126] and [127] are unused :( 
def cascade_leds(np, beacon_value):
    for i in range(NUM_LEDS):
        r = hex_to_rgb_scale(beacon_value[i * 3 + 0])
        g = hex_to_rgb_scale(beacon_value[i * 3 + 1])
        b = hex_to_rgb_scale(beacon_value[i * 3 + 2])
        
        # Move the current LED value to its proper location
        for j in range(i, -1, -1):
            np[j] = (r, g, b) if j == 0 else np[j-1]
            np.write()
            sleep(0.001)  # Adjust the delay for visual effect

# Initialize the WS2812B LED strip
np = neopixel.NeoPixel(Pin(16), NUM_LEDS)  # Assuming GPIO14 is used for data signal

# Set all LEDs to RED
set_leds_color(np, (255, 0, 0))

# Print the SSID of the network we are trying to connect to
print('Connecting to WiFi Network Name:', secrets.SSID)

# Initialize WiFi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # Power up the WiFi chip
print('Waiting for WiFi chip to power up...')
sleep(3)  # Wait three seconds for the chip to power up and initialize

# Connect to the WiFi network
wlan.connect(secrets.SSID, secrets.PASSWORD)
print('Waiting for access point to log us in...')

# Check if connected to the network
max_attempts = 10
attempts = 0
while not wlan.isconnected() and attempts < max_attempts:
    print(f'Attempt {attempts + 1}...')
    sleep(1)
    attempts += 1

if wlan.isconnected():
    print('Success! We have connected to your access point!')
    print('Try to ping the device at', wlan.ifconfig()[0])

    # Set all LEDs to GREEN and wait for 4 seconds
    set_leds_color(np, (0, 255, 0))
    sleep(4)
    
    while True:
        try:

            # Fetch and print the latest NIST Randomness Beacon reading
            beacon_value = fetch_nist_randomness_beacon()
            # The beacon_value should be char[128] containing ascii "0123456789abcdef"
            if beacon_value and len(beacon_value) == 128:
                print('Latest NIST Randomness Beacon reading:', beacon_value)
                # Cascade the LED values
                cascade_leds(np, beacon_value)
            else:
                print('Could not retrieve the NIST Randomness Beacon reading.')
        except Exception as e:
            print('Failed to fetch beacon:', e)
        
        # Wait for 65 seconds before the next iteration
        sleep(65)
else:
    print('Failed to connect to the WiFi network.')

