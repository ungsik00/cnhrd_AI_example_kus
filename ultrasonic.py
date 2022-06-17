import tkinter   as tk
import threading as th
import time      as t
import RPi.GPIO  as GPIO

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
            
            else:
                pass
            
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
