import threading
import pymysql
from datetime import datetime, timedelta

class DBController:
    
    def __init__(self):
        # self.driver_address = None #String
        # self.ipv4_address = None #String
        self.id = 'admin' #String
        self.password = '1234' #String

        self.locker = threading.Lock()
        
        
    def connect(self):
        self.connector = pymysql.connect(host='127.0.0.1', user= self.id, \
             password = self.password, db='smart_vent', charset='utf8')
        self.cursor = self.connector.cursor()
        print('$$ DB is connected')
        
    def disconnect(self):
        self.connector.commit()
        self.connector.close()
        self.connector=None
        self.cursor=None

    def update(self):
        self.locker.acquire()
        # ...
        self.locker.release()
        pass
    
    def select(self):
        self.locker.acquire()
        # ...
        self.locker.release()
        pass
    
    def delete(self):
        self.locker.acquire()
        # ...
        self.locker.release()
        pass
    
    def insert_sensing(self, pm10, pm25, co, co2, form, log):
        self.locker.acquire()
        
        #self.connect()
        
        query = 'INSERT INTO sensing VALUES(0, now(), {}, {}, {}, {}, "");'.format(pm10, pm25, co, co2, form, log)
        self.cursor.execute(query)
        
        self.connector.commit()
        
        
        
        self.locker.release()
        pass
    
    def get_today(self, datatype):
        self.locker.acquire()
        
        self.connect()
        query = 'select time, {} from sensing where time>="{} 00:00:00"'.format(datatype, str(datetime.now().date()))
        
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.locker.release()

        array = []

        for e in result:
            time = e[0].hour*100 + e[0].minute
            array.append({ 'time':time, 'value':e[1]})
            
        return {'data' : array}
    
    
    def get_yesterday(self, datatype):
        self.locker.acquire()
        
        self.connect()
        
        today = datetime.now()
        yester = datetime.now() - timedelta(days=1) 
        
        query = 'select time, {} from sensing where time<"{} 00:00:00" and time>="{} 00:00:00"'.format(datatype, str(today.date()), str(yester.date()))
        
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.locker.release()

        array = []

        for e in result:
            time = e[0].hour*100 + e[0].minute
            array.append({ 'time':time, 'value':e[1]})
            
        return {'data' : array}
        