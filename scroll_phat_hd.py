# Based on https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3731/blob/master/examples/is31fl3731_blink_example.py :
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio

# uncomment next line if you are using Pimoroni Scroll Phat HD LED 17 x 7
from adafruit_is31fl3731.scroll_phat_hd import ScrollPhatHD as Display

# uncomment this line if you use a Pico, here with SCL=GP21 and SDA=GP20.
i2c = busio.I2C(board.GP21, board.GP20)

# uncomment this line board.SCL and board.SDA are defined
# i2c = busio.I2C(board.SCL, board.SDA)

# array pattern in bits; top row-> bottom row, 8 bits in each row
eye_bottom_left = bytearray((
    0b00111000,
    0b01111100,
    0b11111110,
    0b11011110,
    0b11001110,
    0b01111100,
    0b00111000,
    0b00000000,
    0b00000000
    ))

eye_top_left = bytearray((
    0b00111000,
    0b01111100,
    0b11011110,
    0b11001110,
    0b11111110,
    0b01111100,
    0b00111000,
    0b00000000,
    0b00000000
    ))

eye_top_right = bytearray((
    0b00111000,
    0b01111100,
    0b11101110,
    0b11100110,
    0b11111110,
    0b01111100,
    0b00111000,
    0b00000000,
    0b00000000
    ))

eye_bottom_right = bytearray((
    0b00111000,
    0b01111100,
    0b11111110,
    0b11101110,
    0b11100110,
    0b01111100,
    0b00111000,
    0b00000000,
    0b00000000
    ))

display = Display(i2c)

eyes= [eye_bottom_left, eye_top_left, eye_top_right, eye_bottom_right]
shift= [0, 0, 1, 1]

# first load the frame with the arrows; moves the an_arrow to the right in each
# frame

while True:
    for i in range(4):
        offset1 = 0 + shift[i]
        offset2 = 9 + shift[i]
    
        display.sleep(True)  # turn display off while updating blink bits
        display.fill(0)
        for y in range(display.height):
            row = eyes[i][y]
            for x in range(8):
                bit = 1 << (7 - x) & row
                if bit:
                    display.pixel(x + offset1, y, 50, blink=False)
            for x in range(8):
                bit = 1 << (7 - x) & row
                if bit:
                    display.pixel(x + offset2, y, 50, blink=False)
        display.sleep(False)  # turn display on
        time.sleep(3)
