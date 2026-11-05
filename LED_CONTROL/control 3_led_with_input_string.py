from gpiozero import LED

led_red = LED(5)
led_yellow = LED(6)
led_green = LED(13)

while True:
    colour = input("select colour(red/yellow/green): ")

    led_red.off()
    led_yellow.off()
    led_green.off()

    if colour == "red":
        led_red.on()

    elif colour == "yellow":
        led_yellow.on()

    elif colour == "green":
        led_green.on()

    else:
        print("invalid colour")