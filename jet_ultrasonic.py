#!/usr/bin/env python

# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import RPi.GPIO as GPIO
import time

# Pin Definitions:
trig_pin = 13
echo_pin = 18

time_rising = 0
time_falling = 0
dist = 0.0
flag = False


def echo(channel):
    global time_rising, time_falling, flag
    if GPIO.input(echo_pin) == 0 and flag == False:
        time_rising = time.time()
        flag = True
    elif GPIO.input(echo_pin) == 1 and flag == True:
        flag = False
        time_falling = time.time()


def main():
    global dist
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(trig_pin, GPIO.OUT)  # tirgger pins set as output
    GPIO.setup(echo_pin, GPIO.IN)  # echo pin set as input

    # Initial state for LEDs:
    GPIO.output(trig_pin, GPIO.LOW)

    GPIO.add_event_detect(echo_pin, GPIO.BOTH, callback=echo)
    try:
        while True:
            GPIO.output(trig_pin, GPIO.HIGH)
            time.sleep(0.000001)
            GPIO.output(trig_pin, GPIO.LOW)
            time.sleep(0.1)
            dist = -(time_falling - time_rising) * 34000 / 2
            if dist < 1000:
                print(str(dist) + "cm")

    finally:
        GPIO.cleanup()  # cleanup all GPIOs


if __name__ == '__main__':
    main()
