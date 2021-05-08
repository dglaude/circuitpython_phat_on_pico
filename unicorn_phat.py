### Quick and dirty

import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.GP28, 32)
pixels[0] = (100, 0, 0)
pixels[1] = (0, 100, 0)
pixels[2] = (0, 0, 100)
time.sleep(1)
pixels[0] = (0, 0, 0)
pixels[1] = (0, 0, 0)
pixels[2] = (0, 0, 0)

while True:
    for i in range(0, 32):
        pixels[i] = (31, 0, 0)
        time.sleep(0.05)
    for i in range(0, 32):
        pixels[i] = (0, 0, 0)
        time.sleep(0.05)
    for i in range(0, 32):
        pixels[i] = (0, 31, 0)
        time.sleep(0.05)
    for i in range(0, 32):
        pixels[i] = (0, 0, 0)
        time.sleep(0.05)
    for i in range(0, 32):
        pixels[i] = (0, 0, 31)
        time.sleep(0.05)
    for i in range(0, 32):
        pixels[i] = (0, 0, 0)
        time.sleep(0.05)
