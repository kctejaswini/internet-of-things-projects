import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24
LED = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

try:
    while True:
        GPIO.output(TRIG, False)
        time.sleep(0.1)

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            start = time.time()

        while GPIO.input(ECHO) == 1:
            end = time.time()

        distance = (end - start) * 17150

        print("Distance:", round(distance, 2), "cm")

        if distance <= 10:
            GPIO.output(LED, True)
            print("Object Detected - LED ON")
        else:
            GPIO.output(LED, False)

        time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()