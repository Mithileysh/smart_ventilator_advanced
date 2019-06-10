import threading

class SharedData:
    
    def __init__(self):
        self.last_sensing = {}
        self.auto_mode = True
        self.locker = threading.Lock()
        
        self.co2_limit = 1000
        self.co_limit = 10
        # self.pm1_limit = None # no use
        self.pm25_limit = 35
        self.pm10_limit = 100
        
        # safe range
        self.co2_safe = 700
        self.co_safe = 1
        self.pm25_safe = 20
        self.pm10_safe = 30
        pass
    
    def get_limit(self):
        return {'co': self.co_limit, 'co2':self.co2_limit, 'pm10':self.pm10_limit, 'pm25':self.pm25_limit}

    def get_safe(self):
        return {'co': self.co_safe, 'co2':self.co2_safe, 'pm10':self.pm10_safe, 'pm25':self.pm25_safe}
    
    def set_limit(self, dict_data):
        self.locker.acquire()
        
        self.co2_limit = dict_data['co2']
        self.co_limit = dict_data['co']
        # self.pm1_limit = None # no use
        self.pm25_limit = dict_data['pm25']
        self.pm10_limit = dict_data['pm10']
        
        self.locker.release()
        pass
    
    def set_safe(self, dict_data):
        self.locker.acquire()
        
        self.co2_safe = dict_data['co2']
        self.co_safe = dict_data['co']
        # self.pm1_limit = None # no use
        self.pm25_safe = dict_data['pm25']
        self.pm10_safe = dict_data['pm10']
        
        self.locker.release()
        pass

    def set_sensing(self, pm10, pm25, co, co2):
        self.locker.acquire()
        
        self.last_sensing['pm10']=pm10
        self.last_sensing['pm25']=pm25
        self.last_sensing['co']=co
        self.last_sensing['co2']=co2
        
        self.locker.release()
        pass
    
    
    def get_sensing(self):
        return self.last_sensing

datas = SharedData()