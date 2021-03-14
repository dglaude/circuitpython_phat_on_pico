import time
import board
import busio
import digitalio
from adafruit_max7219 import bcddigits

spi_mosi = board.GP3
spi_clk = board.GP2
pin_cs = board.GP5
bt_left = board.GP7     # GPIO 17 = GP7  (11)
bt_right = board.GP14   # GPIO 26 = GP14 (37)

button_l = digitalio.DigitalInOut(bt_left)
button_l.direction = digitalio.Direction.INPUT
button_l.pull = digitalio.Pull.UP

button_r = digitalio.DigitalInOut(bt_right)
button_r.direction = digitalio.Direction.INPUT
button_r.pull = digitalio.Pull.UP

spi = busio.SPI(spi_clk, MOSI=spi_mosi)

cs = digitalio.DigitalInOut(pin_cs)

display = bcddigits.BCDDigits(spi, cs, nDigits=8)
display.clear_all()
display.show_str(0,'8.8.8.8.8.8.8.8.')
#display.show_str(0,'{:9.3f}'.format(-1234.567))
display.show()

old0 = button_l.value
old1 = button_r.value

while True:
    new0 = button_l.value
    new1 = button_r.value

    if old0!=new0:
        display.clear_all()
        if new0:
            display.show()
        else:
            display.show_str(0,'12345678')
            display.show()
        old0 = new0

    if old1!=new1:
        display.clear_all()
        if new1:
            display.show()
        else:
            display.show_str(0,'87654321')
            display.show()
        old1 = new1

    time.sleep(0.01)
