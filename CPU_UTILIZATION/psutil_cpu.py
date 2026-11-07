import psutil
from gpiozero import LED
from time import sleep

led = LED(17)

try:
    while True:
        led.on()
        print("LED ON")

        print("CPU Usage:", psutil.cpu_percent(interval=1), "%")
        print("CPU Count:", psutil.cpu_count())

        sleep(1)

        led.off()
        print("LED OFF")

        print("CPU Usage:", psutil.cpu_percent(interval=1), "%")
        print("CPU Count:", psutil.cpu_count())

        sleep(1)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    led.off()
    led.close()