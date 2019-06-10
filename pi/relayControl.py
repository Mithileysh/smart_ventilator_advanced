import RPi.GPIO as GPIO
import time

INTERVAL = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
print("setup")
time.sleep(2)

for i in range(1, 3):
    GPIO.output(21, True)
    print("true")
    time.sleep(INTERVAL)

    GPIO.output(21, False)
    print("false")
    time.sleep(INTERVAL)

GPIO.cleanup()
print("cleanup")
time.sleep(2)
