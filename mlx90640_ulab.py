# ulab optimisation with the help of @v923z
#
# mlx90640_pygamer learn guide:
# * https://learn.adafruit.com/adafruit-mlx90640-ir-thermal-camera/circuitpython-thermal-camera#
#
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
#
# Adapted by David Glaude for 240x240 screen.
#
# 1) RedRobotics Pico to Zero Adaptor v0.2:
#    * https://www.tindie.com/products/redrobotics/pico-2-pi-adapter-board/
# 2) Raspberry Pi Pico
# 3) 8086net Butterfly
#    * https://www.tindie.com/products/8086net/butterfly/
# 4) Adafruit 240x240 PiMiniTft:
#    * https://shop.pimoroni.com/products/adafruit-mini-pitft-1-3-240x240-tft-add-on-for-raspberry-pi
#    * https://www.adafruit.com/product/4484
# 5) Breakout Garden Mini I2C:
#    * https://shop.pimoroni.com/products/breakout-garden-mini-i2c
# 6) Pimoroni MLX90640 breakout Garden:
#    * https://shop.pimoroni.com/products/mlx90640-thermal-camera-breakout?variant=12536948654163

# This could be more simple with just the "Pico Explorer Base" + the MLX Breakout Garden
# It is not tested but I believe it's only 4 lines that need to be modified.

import time
import board
import busio
import digitalio
import displayio
import terminalio
from adafruit_display_text.label import Label
from simpleio import map_range

import adafruit_st7789
import adafruit_mlx90640

import ulab

tft_cs = board.GP5
tft_dc = board.GP22
spi_mosi = board.GP3
spi_clk = board.GP2
#
# For "Pico Explorer Base" replace the line above by the line bellow
#
# tft_cs = board.GP17
# tft_dc = board.GP16
# spi_mosi = board.GP19
# spi_clk = board.GP18

# Release any resources currently in use for the displays
displayio.release_displays()

spi = busio.SPI(spi_clk, MOSI=spi_mosi)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)

# Create the ST7789 display:
display = adafruit_st7789.ST7789(
    display_bus,
    width=240,
    height=240,
    rowstart=80,
    colstart=0,
    rotation=180,
    auto_refresh=False
)

number_of_colors = 64  # Number of color in the gradian
last_color = number_of_colors - 1  # Last color in palette
palette = displayio.Palette(number_of_colors)  # Palette with all our colors

## Heatmap code inspired from: http://www.andrewnoske.com/wiki/Code_-_heatmaps_and_color_gradients
color_A = [
    [0, 0, 0],
    [0, 0, 255],
    [0, 255, 255],
    [0, 255, 0],
    [255, 255, 0],
    [255, 0, 0],
    [255, 255, 255],
]
color_B = [[0, 0, 255], [0, 255, 255], [0, 255, 0], [255, 255, 0], [255, 0, 0]]
color_C = [[0, 0, 0], [255, 255, 255]]
color_D = [[0, 0, 255], [255, 0, 0]]

color = color_B
NUM_COLORS = len(color)

def MakeHeatMapColor():
    for c in range(number_of_colors):
        value = c * (NUM_COLORS - 1) / last_color
        idx1 = int(value)  # Our desired color will be after this index.
        if idx1 == value:  # This is the corner case
            red = color[idx1][0]
            green = color[idx1][1]
            blue = color[idx1][2]
        else:
            idx2 = idx1 + 1  # ... and before this index (inclusive).
            fractBetween = value - idx1  # Distance between the two indexes (0-1).
            red = int(
                round((color[idx2][0] - color[idx1][0]) * fractBetween + color[idx1][0])
            )
            green = int(
                round((color[idx2][1] - color[idx1][1]) * fractBetween + color[idx1][1])
            )
            blue = int(
                round((color[idx2][2] - color[idx1][2]) * fractBetween + color[idx1][2])
            )
        palette[c] = (0x010000 * red) + (0x000100 * green) + (0x000001 * blue)

MakeHeatMapColor()

# Bitmap for colour coded thermal value
image_bitmap = displayio.Bitmap(24, 32, number_of_colors)

# Create a TileGrid using the Bitmap and Palette
image_tile = displayio.TileGrid(image_bitmap, pixel_shader=palette)

# Create a Group that scale 24*32 to 168*224
image_group = displayio.Group(scale=7)
image_group.append(image_tile)

scale_bitmap = displayio.Bitmap(1, number_of_colors, number_of_colors)
scale_group = displayio.Group(scale=3)
scale_tile = displayio.TileGrid(scale_bitmap, pixel_shader=palette, x=69, y=8)
scale_group.append(scale_tile)

for i in range(number_of_colors):
    scale_bitmap[0, i] = i  # Fill the scale with the palette gradian

# Create the super Group
group = displayio.Group()

min_label = Label(terminalio.FONT, scale=2, max_glyphs=10, color=palette[0], x=180, y=10)
max_label = Label(terminalio.FONT, scale=2, max_glyphs=10, color=palette[last_color], x=180, y=230)

# Add all the sub-group to the SuperGroup
group.append(image_group)
group.append(scale_group)
group.append(min_label)
group.append(max_label)

# Add the SuperGroup to the Display
display.show(group)

#i2c = busio.I2C(board.GP21, board.GP20, frequency=800000)
i2c = busio.I2C(board.GP21, board.GP20, frequency=1000000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

#mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_0_5_HZ
#mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
#mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4/8/16/32_HZ

frame = [0] * 768
####npframe = ulab.zeros(768)

while True:
    stamp = time.monotonic()
    try:
        mlx.getFrame(frame)
####        mlx.getFrame(npframe)
#### getFrame is faster with an array as input than with a ulab.array as input
    except ValueError:
        # these happen, no biggie - retry
        continue

#    print("Time for data aquisition: %0.2f s" % (time.monotonic()-stamp))

# Convert in ulab.array, find the min and max and normalize to int from 0 to last_color.
    npframe=ulab.array(frame)
    min_t=ulab.numerical.min(npframe)
    max_t=ulab.numerical.max(npframe)
    factor=last_color/(max_t-min_t)
    inta=ulab.array((npframe-min_t)*factor,dtype=ulab.int8)

    stamp_copy = time.monotonic()
##    int_bitmap=inta.reshape((24,32))
    index = 0
    for h in range(24):
        for w in range(32):
##            image_bitmap[h, w] = int_bitmap[h, w]
#            image_bitmap[h, w] = inta[w+(h<<5)]
#            image_bitmap[h, w] = inta[h*32+w]
            image_bitmap[h, w] = inta[index]
            index+=1

    print("Time copy: %0.2f s" % (time.monotonic()-stamp_copy))

    min_label.text = "%0.1f" % (min_t)
    max_label.text = "%0.1f" % (max_t)

    display.refresh()
#    print("Total time for aquisition and display %0.2f s" % (time.monotonic()-stamp))
