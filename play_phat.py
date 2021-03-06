#### Anavi Play pHAT
import time
import board
import digitalio
import gamepad

"""
GPIO 22 = GP9  (15) : Button UP	15
GPIO 27 = GP8  (13) : Button DOWN	13
GPIO  4 = GP6  ( 7) : Button LEFT	7
GPIO 17 = GP7  (11) : Button RIGHT	11
GPIO  5 = GP10 (29) : Button START	29
GPIO  6 = GP11 (31) : Button SELECT	31
GPIO 19 = GP13 (35) : Button A	35
GPIO 26 = GP14 (37) : Button B	37
"""

B_Up     = 1 << 0
B_Down   = 1 << 1
B_Left   = 1 << 2
B_Right  = 1 << 3
B_Start  = 1 << 4
B_Select = 1 << 5
B_A      = 1 << 6
B_B      = 1 << 7

pad = gamepad.GamePad(
    digitalio.DigitalInOut(board.GP9),
    digitalio.DigitalInOut(board.GP8),
    digitalio.DigitalInOut(board.GP6),
    digitalio.DigitalInOut(board.GP7),
    digitalio.DigitalInOut(board.GP10),
    digitalio.DigitalInOut(board.GP11),
    digitalio.DigitalInOut(board.GP13),
    digitalio.DigitalInOut(board.GP14),
)

while True:
    buttons = pad.get_pressed()
    if buttons & B_Up:
        print("UP")
    elif buttons & B_Down:
        print("DOWN")
    elif buttons & B_Left:
        print("LEFT")
    elif buttons & B_Right:
        print("RIGHT")
    elif buttons & B_Start:
        print("Start")
    elif buttons & B_Select:
        print("Select")
    elif buttons & B_A:
        print("A")
    elif buttons & B_B:
        print("B")
    time.sleep(0.05)

    while buttons:
        # Wait for all buttons to be released.
        buttons = pad.get_pressed()
        time.sleep(0.05)
