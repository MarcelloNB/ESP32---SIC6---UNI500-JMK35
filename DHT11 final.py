from machine import Pin
import ujson
import utime as time
import time
import dht
import urequests as requests
import network
import utime

DEVICE_ID = "esp32"
TOKEN = "BBUS-HHBn0mAWD88eOYy32LPIxymHwLrtiJ"
SSID = "elno"
PASS = "Vilani#01"
URL_SERVER = "http://192.168.1.108:1280/sensor1"
movement_count = 0

def do_connect():
    # Initialize Wi-Fi in station mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)  # Activate the Wi-Fi interface

    # Check if already connected
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASS)  # Connect to the Wi-Fi network

        # Wait for connection (timeout after 20 seconds)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            print("Waiting for connection...")
            time.sleep(1)
            timeout -= 1

        if wlan.isconnected():
            print("Connected to Wi-Fi!")
            print("Network config:", wlan.ifconfig())
        else:
            print("Failed to connect to Wi-Fi. Please check credentials or network availability.")
    else:
        print("Already connected to Wi-Fi!")
        print("Network config:", wlan.ifconfig())

    
        
def send_data_ubidots(temperature, humidity, movement_count):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_ID
    headers = {"Content-Type": "application/json", "X-Auth-Token": TOKEN}
    data = {
        "temp": temperature,
        "humidity": humidity,
        "movement" : movement_count
    }
    
    retries = 3
    for i in range(retries):
        try:
            print("Sending data to ubidots...")
            response = requests.post(url, json=data, headers=headers, timeout=10)
            print("Response status code:", response.status_code)
            print("Response text:", response.text)
            response.close()
            break
        except Exception as e:
            print("Attempt", i + 1, "failed:", e)
            time.sleep(5)  # Wait before retrying

# Function to format the current timestamp
def get_current_timestamp():
    # Get current time in seconds since the Epoch
    current_timestamp = utime.time()
    
    # Convert timestamp to a tuple (year, month, day, hour, minute, second, weekday, yearday)
    time_tuple = utime.localtime(current_timestamp)
    
    # Format the time tuple into a string (e.g., "2023-10-15 12:34:56")
    formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        time_tuple[0], time_tuple[1], time_tuple[2],  # Year, Month, Day
        time_tuple[3], time_tuple[4], time_tuple[5]   # Hour, Minute, Second
    )
    return formatted_time
            
def send_data_server(temperature, humidity):
    url = URL_SERVER
    headers = {"Content-Type": "application/json"}
    
        # Get the current timestamp
    timestamp = get_current_timestamp()
    
    data = {
        "Temperature": temperature,
        "Humidity": humidity,
        "timestamp" : timestamp
    }
    
    retries = 3
    for i in range(retries):
        try:
            print("Sending data to server...")
            response = requests.post(url, json=data, headers=headers, timeout=30)
            print("Response status code:", response.status_code)
            print("Response text:", response.json)
            response.close()
            break
        except Exception as e:
            print("Attempt", i + 1, "failed:", e)
            time.sleep(5)  # Wait before retrying

def monitor_pir_sensor():
    global movement_count  # Menggunakan variabel global
    while True:
        
        if (pir_sensor.value() == 1):  # Jika PIR mendeteksi gerakan
            led.value(1)
            print("Motion detected!")
            movement_count += 1
            
            return True
        else:
            led.value(0)
            print("No motion detected.")
            time.sleep(0.5)  # Tunggu 1 detik sebelum memeriksa lagi
            return False
        
#sensor initialize
led= Pin(2, Pin.OUT)
sensor = dht.DHT11(Pin(13))
pir_sensor= Pin(12, Pin.IN)
try:
    do_connect()  # Hubungkan ke Wi-Fi    
except RuntimeError as e:
    print(e)
    # Handle Wi-Fi connection failure (e.g., retry or exit)

while True:
    try:
        monitor_pir_sensor()  # Cek sensor PIR
        sensor.measure()  # Ambil data suhu dan kelembapan
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Movement Count: {movement_count}")
        
        # Kirim data ke Ubidots dan server
        send_data_ubidots(temperature, humidity, movement_count)
        send_data_server(temperature, humidity)
        
        time.sleep(10)  # Tunggu 60 detik sebelum memeriksa lagi
        
            
    except Exception as e:
        print("Error in main loop:", e)
        time.sleep(5) 
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        