"""
adapted from http://helloraspberrypi.blogspot.com/2021/01/raspberry-pi-picocircuitpython-st7789.html
"""

import board
import time
import digitalio
import displayio
import busio
import adafruit_st7789

import terminalio
from adafruit_display_text import label

bt_up = board.GP27
bt_down = board.GP26

button_0= digitalio.DigitalInOut(bt_up)
button_0.direction = digitalio.Direction.INPUT
button_0.pull = digitalio.Pull.UP

button_1 = digitalio.DigitalInOut(bt_down)
button_1.direction = digitalio.Direction.INPUT
button_1.pull = digitalio.Pull.UP

# Release any resources currently in use for the displays
displayio.release_displays()

tft_cs = board.GP5
tft_dc = board.GP22
#tft_res = board.GP23
spi_mosi = board.GP3
spi_clk = board.GP2

spi = busio.SPI(spi_clk, MOSI=spi_mosi)

display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs
)

# Create the ST7789 display:
display = adafruit_st7789.ST7789(
    display_bus,
    width=240,
    height=240,
    rowstart=80,
    colstart=0,
    rotation=180,
)

group = displayio.Group(max_size=10)
display.show(group)

bitmap = displayio.Bitmap(240, 240, 240)

palette = displayio.Palette(240)
for p in range(240):
    palette[p] = (0x010000*p) + (0x0100*p) + p

for y in range(240):
    for x in range(240):
        bitmap[x,y] = y

tileGrid = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)
group.append(tileGrid)

# Draw a label
text_group = displayio.Group(max_size=10, scale=16, x=10, y=120)
text = "??"
text_area = label.Label(terminalio.FONT, text=text, color=0xFF0000)
text_group.append(text_area)  # Subgroup for text scaling

group.append(text_group)

old0 = button_0.value
old1 = button_1.value

while True:
    new0 = button_0.value
    new1 = button_1.value

    if old0!=new0:
        if new0:
            text_area.text = ""
        else:
            text_area.text = "23"
        old0 = new0

    if old1!=new1:
        if new1:
            text_area.text = ""
        else:
            text_area.text = "24"
        old1 = new1

    time.sleep(0.01)
