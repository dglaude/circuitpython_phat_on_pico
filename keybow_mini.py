import time
import board
import digitalio
import adafruit_dotstar

button_0= digitalio.DigitalInOut(board.GP11)
button_0.direction = digitalio.Direction.INPUT
button_0.pull = digitalio.Pull.UP
 
button_1 = digitalio.DigitalInOut(board.GP9)
button_1.direction = digitalio.Direction.INPUT
button_1.pull = digitalio.Pull.UP

button_2 = digitalio.DigitalInOut(board.GP7)
button_2.direction = digitalio.Direction.INPUT
button_2.pull = digitalio.Pull.UP

pixels = adafruit_dotstar.DotStar(board.GP2, board.GP3, 3)
pixels[0] = (100, 0, 0)
pixels[1] = (0, 100, 0)
pixels[2] = (0, 0, 100)
time.sleep(1)
pixels[0] = (0, 0, 0)
pixels[1] = (0, 0, 0)
pixels[2] = (0, 0, 0)

old0 = button_0.value
old1 = button_1.value
old2 = button_2.value

while True:
    new0 = button_0.value
    new1 = button_1.value
    new2 = button_2.value
    
    if old0!=new0:
        if new0:
            pixels[0] = (0, 0, 0)
        else:
            pixels[0] = (100, 0, 0)
        old0 = new0

    if old1!=new1:
        if new1:
            pixels[1] = (0, 0, 0)
        else:
            pixels[1] = (0, 100, 0)
        old1 = new1

    if old2!=new2:
        if new2:
            pixels[2] = (0, 0, 0)
        else:
            pixels[2] = (0, 0, 100)
        old2 = new2
    
    time.sleep(0.05)
