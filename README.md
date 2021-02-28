# circuitpython_phat_on_pico
Trying to drive pHAT plugged on a Pico with CircuitPython

I have a lot of pHAT designed for the Raspberry Pi Zero (or full size SBC Raspberry).
There is now a MCU from Raspberry Pi, the Raspberry PICO.

Multiple people/company are working on provinding board based on RP2040 (the MCU of the PICO) that have a Raspberry Pi pinout by mapping pin of the PICO/RP2040 to pin on the de facto 20x2 pinout.

The board I use is "Pico to Zero adaptor v0.2" by RED ROBOTICS.

## Keybow mini

Board reference: https://pinout.xyz/pinout/keybow_mini#

Pin mapping for "Pico to Zero adaptor v0.2":
* GPIO 17 = pin 11 = Key 1 => GP7
* GPIO 22 = pin 15 = Key 2 => GP9
* GPIO 10 = pin 19 = LEDs data => GP3
* GPIO 11 = pin 23 = LEDs clock => GP2
* GPIO  6 = pin 31 = Key 3 => GP11

Example code: keybow_mini.py
