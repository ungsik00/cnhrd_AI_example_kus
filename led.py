import Jetson.GPIO  as GPIO
import time as t

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, GPIO.HIGH)
t.sleep(5)
GPIO.output(23, GPIO.LOW)            
GPIO.cleanup()
