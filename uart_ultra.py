import RPi.GPIO as GPIO
import serial
import threading as th
import time

serial_port = None

def echo(channel):
    global time_rising, time_falling, flag
    if GPIO.input(18) == 0 and flag == False:
        time_rising = time.time()
        flag = True
    elif GPIO.input(18) == 1 and flag == True:
        flag = False
        time_falling = time.time()


def uart():
    global speed, serial_port

    while True:
        if (dist < 40 and dist > 20) or (dist < 15 and dist > 5):
            if dist > 20:
                speed = (dist - 20) * 5 / 2 + 50
            elif dist < 15:
                speed = (dist - 5) * 4 + 10

            serial_port.write((str(int(speed)) + "." + str(int(speed)) + "." + str(int(speed)) + "." + str(int(speed)) + "\n").encode())
            print(str(int(speed)))
        else:
            serial_port.write((str(int(50)) + "." + str(int(50)) + "." + str(int(50)) + "." + str(int(50)) + "\n").encode())
            print('stop')

        time.sleep(0.5)

# Pin Definitions:
trig_pin = 13
echo_pin = 18

time_rising = 0
time_falling = 0
dist = 0.0
flag = False
speed = 0


if __name__ == '__main__':
    try:
        dist = 0.0
        # Serial port Definition
        serial_port = serial.Serial(
            port="/dev/ttyTHS1",
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        time.sleep(1)

        # Pin Setup:
        GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
        GPIO.setwarnings(False)
        GPIO.setup(13, GPIO.OUT)  # trigger pins set as output
        GPIO.setup(18, GPIO.IN)  # echo pin set as input

        # Initial state for LEDs:
        GPIO.output(trig_pin, GPIO.LOW)

        GPIO.add_event_detect(18, GPIO.BOTH, callback=echo)

        print("Jetson Nano On")
        serial_port.write("Jetson Nano On\n".encode())
        time.sleep(0.1)

        buf = ""
        # Send a simple header
        while True:
            if serial_port.inWaiting() > 0:
                data = serial_port.read()
                buf = buf + data.decode()
                if data == "\n".encode() or data == "\r".encode():
                    print(buf)
                    if buf == "Stm32 On\n":
                        break
                    #buf = ""

        time.sleep(1)

        #ultra_thread = th.Thread(target=ultrasonic)
        uart_thread = th.Thread(target=uart)
        #ultra_thread.start()
        uart_thread.start()

        while True:
            GPIO.output(13, GPIO.HIGH)
            time.sleep(0.000001)
            GPIO.output(13, GPIO.LOW)
            time.sleep(0.1)
            if flag == False or flag == True:
                dist = -(time_falling - time_rising) * 34000 / 2
                #if dist < 1000:
                #print(str(dist) + "cm")

    finally:
        GPIO.cleanup()  # cleanup all GPIOs
        serial_port.write(("stop " + str(int(0)) + "\n").encode())
        time.sleep(0.1)
        serial_port.write("Exiting Program\n".encode())
        print("Exiting Program")
        serial_port.close()
        pass


