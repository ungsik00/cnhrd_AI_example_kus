#!/usr/bin/python3
import time
import serial

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
# Wait a second to let the port initialize
time.sleep(1)

print("Jetson Nano On")
serial_port.write("Jetson Nano On\n".encode())
time.sleep(0.1)

buf_flag = False

try:
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

    serial_port.write("go\n".encode())
    time.sleep(1)
    serial_port.write("stop\n".encode())
    time.sleep(1)

except KeyboardInterrupt:
    pass

except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.write("Exiting Program\n".encode())
    print("Exiting Program")
    serial_port.close()
    pass
