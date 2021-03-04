###
### Braincraft on a Pico To Zero Adaptor v0.2
### Working: Backlight+Fan+DotStar+Buttons+DisplayIO
###

import time
import board
import digitalio
import gamepad
import adafruit_dotstar as dotstar
import displayio
import busio
import adafruit_st7789

# Backlight

"""
GPIO #26 (37) GP14 - Backlight
"""

print("BACKLIGHT")

backlight = digitalio.DigitalInOut(board.GP14)
backlight.direction=digitalio.Direction.OUTPUT

backlight.value=True
time.sleep(1)
backlight.value=False
time.sleep(1)
backlight.value=True

# FAN

"""
GPIO #4 (7) GP6 - FAN.
"""

print("FAN")

fan = digitalio.DigitalInOut(board.GP6)
fan.direction=digitalio.Direction.OUTPUT

fan.value=True
time.sleep(3)
fan.value=False

# DotStar

"""
GPIO #5 (29) GP10 - DotStar LED data pin.
GPIO #6 (31) GP11 - Dotstar LED clock pin.
"""

print("DOTSTAR")

dots = dotstar.DotStar(board.GP11, board.GP10, 3, brightness=0.2)

time.sleep(1)
dots[0] = (255, 0, 0)
time.sleep(1)
dots[1] = (0, 255, 0)
time.sleep(1)
dots[2] = (0, 0, 255)
time.sleep(1)
dots.fill((0, 0, 0))

# Buttons

"""
GPIO #17 (11) GP7  - Button
GPIO #16 (36) GP17 - Joystick select
GPIO #22 (15) GP9  - Joystick left
GPIO #23 (16) GP27 - Joystick up
GPIO #24 (18) GP26 - Joystick right
GPIO #27 (13) GP8  - Joystick down
"""

print("BUTTONS (Konami code)")

B_A = 1 << 0
B_B = 1 << 1
B_LEFT   = 1 << 2
B_UP     = 1 << 3
B_RIGHT  = 1 << 4
B_DOWN   = 1 << 5

pad = gamepad.GamePad(
    digitalio.DigitalInOut(board.GP7),
    digitalio.DigitalInOut(board.GP17),
    digitalio.DigitalInOut(board.GP9),
    digitalio.DigitalInOut(board.GP27),
    digitalio.DigitalInOut(board.GP26),
    digitalio.DigitalInOut(board.GP8),
)

konami = [B_UP, B_UP, B_DOWN, B_DOWN, B_LEFT, B_RIGHT, B_LEFT, B_RIGHT, B_B, B_A]
position = 0

while True:
    buttons = pad.get_pressed()
    if buttons != 0:
        if konami[position] == buttons:
            dots[position%3]=(0,0,0)
            position += 1
            dots[position%3]=(255,0,0)
            if position == len(konami):
                print("Konami!")
                break
        else:
            dots[position%3]=(0,0,0)
            position = 0
            dots[position%3]=(0,0,255)
    if buttons & B_A:
        print("A")
    elif buttons & B_B:
        print("B")
    elif buttons & B_LEFT:
        print("LEFT")
    elif buttons & B_UP:
        print("UP")
    elif buttons & B_RIGHT:
        print("RIGHT")
    elif buttons & B_DOWN:
        print("DOWN")
    time.sleep(0.05)

    while buttons:
        # Wait for all buttons to be released.
        buttons = pad.get_pressed()
        time.sleep(0.05)

dots.fill((0, 0, 0))

# DisplayIO

"""
adapted from http://helloraspberrypi.blogspot.com/2021/01/raspberry-pi-picocircuitpython-st7789.html
"""

print("DISPLAYIO")

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

bitmap = displayio.Bitmap(240, 240, 135)

palette = displayio.Palette(240)
for p in range(240):
    palette[p] = (0x10000*p) + (0x100*p) + p

for y in range(240):
    for x in range(240):
        bitmap[x,y] = y

tileGrid = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)
group.append(tileGrid)

time.sleep(3.0)

while True:
    for p in range(240):
        palette[p] = p
    time.sleep(1)
    for p in range(240):
        palette[p] = p * 0x100
    time.sleep(1)
    for p in range(240):
        palette[p] = p * 0x10000
    time.sleep(1)

###########################################

# I2SOut does not work due to pin selection
# I2SIn not supported by CircuitPython

"""
GPIO #18, GPIO#19, GPIO #20, GPIO #21 - I2S Digital Audio.

GPIO #18 (PCM CLK)  GP28
GPIO #19 (PCM FS)   GP13
#GPIO #20 (PCM DIN) GP16
GPIO #21 (PCM DOUT) GP15

classaudiobusio.I2SOut(
    bit_clock: microcontroller.Pin, 
    word_select: microcontroller.Pin, 
    data: microcontroller.Pin, *, 
    left_justified: bool)
"""

"""
import array
import math
import audiocore
import audiobusio
"""

"""
tone_volume = 0.1  # Increase this to increase the volume of the tone.
frequency = 440  # Set this to the Hz of the tone you want to generate.
length = 8000 // frequency
sine_wave = array.array("h", [0] * length)
for i in range(length):
    sine_wave[i] = int((math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 -1))

audio = audiobusio.I2SOut(board.GP28, board.GP13, board.GP15)

sine_wave_sample = audiocore.RawSample(sine_wave)

while True:
    audio.play(sine_wave_sample, loop=True)
    time.sleep(1)
    audio.stop()
    time.sleep(1)
"""
