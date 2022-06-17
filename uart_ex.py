import tkinter   as tk
import threading as th
import time      as t
import RPi.GPIO  as GPIO
import serial

'''
def updataUsc():
    global dist
'''    

    
if __name__ == "__main__":
    try:
        dist = 0
        time_rising = 0
        time_falling = 0

        trig = 23
        echo = 24
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(24, GPIO.IN)
        serial_port = serial.Serial(
            port="/dev/ttyTHS1",
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
        )
        # Wait a second to let the port initialize
        t.sleep(1)

        print("UART Demonstration Progr11am")
        serial_port.write("UART Demonst11ration Program\n".encode())
        t.sleep(0.1)

        print("NVIDIA Jetson Nano Developer Kit")
        serial_port.write("NVIDIA Jetson Nano Developer Kit\n".encode())
        t.sleep(0.1)

        while True:
            GPIO.output(trig, GPIO.LOW)
            t.sleep(0.1)
            GPIO.output(trig, GPIO.HIGH)
            t.sleep(0.000001)
            GPIO.output(trig, GPIO.LOW)
            
            while GPIO.input(echo) == 0 :
                time_rising = t.time()
            while GPIO.input(echo) == 1 :
                time_falling = t.time()
            
            
            dist = time_falling - time_rising
            dist *= 34000 / 2
            dist = int(dist)
            
            if dist < 1000 : 
                print(str(dist) + 'cm')
                buf = str(dist) + 'cm' + '\n'
                serial_port.write(buf.encode())
            
            else:
                pass
            
    except KeyboardInterrupt:
        serial_port.write("Exiting Program\n".encode()) 
        print("Exiting Program")
        pass
    finally:
        serial_port.close()
        GPIO.cleanup()
