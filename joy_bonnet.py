#### I2C fail because there is not Pull Up resistor

##### SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
##### SPDX-License-Identifier: MIT
#####import busio
####import adafruit_ads1x15.ads1015 as ADS
####from adafruit_ads1x15.analog_in import AnalogIn
####
####sda = board.GP20
####scl = board.GP21
##### Create the I2C bus
####i2c = busio.I2C(scl, sda)
##### Create the ADC object using the I2C bus
####ads = ADS.ADS1015(i2c)
##### Create single-ended input on channel 0
####chan = AnalogIn(ads, ADS.P0)
##### Create differential input between channel 0 and 1
##### chan = AnalogIn(ads, ADS.P0, ADS.P1)
####print("{:>5}\t{:>5}".format("raw", "v"))
####while True:
####    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
####    time.sleep(0.5)

import time
import board
import digitalio
import gamepad

"""
I2C 0x48: ADS1015
GPIO  2 = GP20 ( 3) : SDA
GPIO  3 = GP21 ( 5) : SCL
GPIO 22 = GP9  (15) : Player1
(16) GPIO 23 = GP27 : Player2
GPIO  6 = GP11 (31) : ButtonB
(32) GPIO 12 = GP18 : ButtonA
GPIO 13 = GP12 (33) : ButtonY
(36) GPIO 16 = GP17 : ButtonX
GPIO 26 = GP14 (37) : Start
(38) GPIO 20 = GP16 : Select
"""


B_Player2 = 1 << 0
B_Player1 = 1 << 1
B_ButtonB = 1 << 2
B_ButtonA = 1 << 3
B_ButtonY = 1 << 4
B_ButtonX = 1 << 5
B_Start   = 1 << 6
B_Select  = 1 << 7

pad = gamepad.GamePad(
    digitalio.DigitalInOut(board.GP9),
    digitalio.DigitalInOut(board.GP27),
    digitalio.DigitalInOut(board.GP11),
    digitalio.DigitalInOut(board.GP18),
    digitalio.DigitalInOut(board.GP12),
    digitalio.DigitalInOut(board.GP17),
    digitalio.DigitalInOut(board.GP14),
    digitalio.DigitalInOut(board.GP16),
)

while True:
    buttons = pad.get_pressed()
    if buttons & B_Player1:
        print("1")
    elif buttons & B_Player2:
        print("2")
    elif buttons & B_ButtonB:
        print("B")
    elif buttons & B_ButtonA:
        print("A")
    elif buttons & B_ButtonY:
        print("Y")
    elif buttons & B_ButtonX:
        print("X")
    elif buttons & B_Start:
        print("Start")
    elif buttons & B_Select:
        print("Select")
    time.sleep(0.05)

    while buttons:
        # Wait for all buttons to be released.
        buttons = pad.get_pressed()
        time.sleep(0.05)
