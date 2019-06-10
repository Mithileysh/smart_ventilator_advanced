import threading
import RPi.GPIO as GPIO

class FanController:
    
    def __init__(self):
        self._is_on = False
        self._auto_mode = True
        
        self.pin_number = 21 #Integer
        
        self.locker = threading.Lock()
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_number, GPIO.OUT)
        
        self.off()
        pass #pin_number=pin
    
    def on(self):
        self.locker.acquire()
        
        self._is_on = True
        GPIO.output(self.pin_number, True)
        
        self.locker.release()
        pass # on fan
    
    def off(self):
        self.locker.acquire()
        
        self._is_on = False
        GPIO.output(self.pin_number, False)
        
        self.locker.release()
        pass # off fan
    
    def is_on(self):
        return self._is_on
    
    def on_auto_mode(self):
        self.locker.acquire()
        self._auto_mode = True
        self.locker.release()
        pass
    
    def off_auto_mode(self):
        self.locker.acquire()
        self._auto_mode = False
        self.locker.release()
    
    def is_auto_mode(self):
        return self._auto_mode
    