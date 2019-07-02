from db_control import DBController
from fan_control import FanController
import shared_data

import mh_z19 as co2
import ze07_co_uart as co
import pms7003 as pm
import ze07_form_uart as form

import datetime
import time

#flag
PRINT_SENSING_LOG = True
#DB_INSERT_INTERVAL_SEC = 1800

class SensingHandler:

    def __init__(self, fan, db):
        self.db_controller = db #DBController
        self.fan_controller = fan #FanController
        
        self.send_db_interval = None
        self.send_app_interval = None
    
    
    def start(self):
        print('## Sensing is Running ##')
        now_minute = datetime.datetime.now().minute
        start_minute = 0
        
        if now_minute < 30:
            start_minute = 30
        else:
            start_minute = 0


        while True:
            
            try:
                co2_value = co2.read()['co2']
                co_value = co.read()
                pm_values = pm.read()
                form_value = form.read()
                
                if self.fan_controller.is_auto_mode():
                    if self.fan_controller.is_on():
                        print('fan is on')
                        if shared_data.datas.co2_safe >= co2_value \
                        and shared_data.datas.co_safe >= co_value \
                        and shared_data.datas.pm25_safe >= pm_values['pm2.5'] \
                        and shared_data.datas.pm10_safe >= pm_values['pm10'] \
                        and shared_data.datas.form_safe >= form_value:
                            print('@ try off')
                            self.fan_controller.off()
                            pass
                        pass
                        
                    else: # is off
                        print('fan is off')
                        if shared_data.datas.co2_limit <= co2_value \
                        or shared_data.datas.co_limit <= co_value \
                        or shared_data.datas.pm25_limit <= pm_values['pm2.5'] \
                        or shared_data.datas.pm10_limit <= pm_values['pm10'] \
                        or shared_data.datas.form_limit <= form_value: 
                            self.fan_controller.on()
                            pass
                        pass
                    
                if self.fan_controller.is_auto_mode():
                    print('is auto mode')
                else:
                    print('is not auto mode')
                            
                #test begin
                if PRINT_SENSING_LOG:                    
                    print('co2: {}'.format(co2_value))
                    print('co: {}'.format(co_value))
                    #print('pm1.0: {}'.format(pm_values['pm1.0']))
                    print('pm2.5: {}'.format(pm_values['pm2.5']))
                    print('pm10: {}'.format(pm_values['pm10']))
                    print('form: {}'.format(form_value))
                    print('')
                #test end
                
                shared_data.datas.set_sensing(pm_values['pm1.0'], \
                                              pm_values['pm2.5'], \
                                              co_value, co2_value, \
                                              form_value)
                
                
                now_minute = datetime.datetime.now().minute
                if start_minute==now_minute:
                    if start_minute == 0:
                        start_minute = 30
                        pass
                    else:
                        start_minute = 0
                        pass
                    
                    self.db_controller.insert_sensing \
                      (pm10=pm_values['pm10'], \
                       pm25=pm_values['pm2.5'], \
                       co=co_value, co2=co2_value, form=form_value, log='')
                    pass
                
                    
            except:
                pass    