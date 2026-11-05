from gpiozero import MotionSensor, LED, OutputDevice
from time import sleep

pir = MotionSensor(17)
led = LED(27)
buzzer = OutputDevice(22, active_high=True)

print("PIR Sensor Initializing...")
sleep(30)

print("House Intrusion Detection System Started")

try:
    while True:
        if pir.motion_detected:
            print("Motion Detected!")
            led.on()
            buzzer.on()
        else:
            print("No Motion Detected")
            led.off()
            buzzer.off()

        sleep(1)

except KeyboardInterrupt:
    print("Program Stopped")

finally:
    led.off()
    buzzer.off()