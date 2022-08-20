import Adafruit_DHT
import time
import requests
import RPi.GPIO as GPIO

TOKEN = "BBFF-thUhhRPJojoHiUB78bozuZuPy2dKTv"  # Put your TOKEN here
DEVICE_LABEL = "week10"  # Put your device label here 
VARIABLE_LABEL_1 = "temperatur"  # Put your first variable label here
VARIABLE_LABEL_2 = "kelembapan"  # Put your second variable label here


def build_payload(variable_1, variable_2):
    # Creates two random values for sending data

    sensor = Adafruit_DHT.DHT11
    pin = 4
    kelembapan, temperatur = Adafruit_DHT.read_retry(sensor, pin)
    
    value_1 = temperatur
    value_2 = kelembapan
    
    payload = {
        variable_1: value_1,
        variable_2: value_2
    }
    
    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2)
    print(payload)
    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if _name_ == '_main_':
    while (True):
        main()
        time.sleep(1)
