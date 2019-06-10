from fan_control import FanController
from db_control import DBController
import os

import json
import socket
import shared_data

class SocketHandler:
    
    def __init__(self, fan, db):
        port = 12345 #Integer
        self.fan_controller = fan #FanController
        self.db_controller = db #Database Controller
        
        os.system('sudo fuser -k -n tcp {}'.format(port))
        
        self.server_socket=socket.socket()#(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind( ('', port) )
        self.server_socket.listen(5)
        pass
    

    def start(self):
        print('## Server is Running ##')
        
        while True:
            try:
                print('\n# Server is Alive #\n')
                client_socket, address = self.server_socket.accept()
                
                print('@ client connected {}'.format(address))
                json_data = client_socket.recv(65535)
                dict_data = json.JSONDecoder().decode(json_data.decode())
                
                cmd = dict_data['command']
                print('### command: {} ###'.format(cmd))
                
                if cmd == 'on_fan':
                    if self.fan_controller.is_auto_mode():
                        print('!!on_fan is not available in auto mode')
                        pass
                    else:
                        if not self.fan_controller.is_on():
                            self.fan_controller.on()
                        
                elif cmd == 'off_fan':
                    if self.fan_controller.is_auto_mode():
                        print('!!off_fan is not available in auto mode')
                        pass                
                    else:
                        if self.fan_controller.is_on():
                            self.fan_controller.off()
                        
                elif cmd == 'check_fan':
                    data_to_send = {'fan_on': self.fan_controller.is_on()}
                    boom = json.JSONEncoder().encode(data_to_send).encode()
                    client_socket.sendall(boom)
                    pass
                
                elif cmd == 'check_auto':
                    data_to_send = {'auto_on':self.fan_controller.is_auto_mode()}
                    boom = json.JSONEncoder().encode(data_to_send).encode()
                    client_socket.sendall(boom)
                    pass
                
                elif cmd == 'on_auto':
                    self.fan_controller.on_auto_mode()
                    pass
                
                elif cmd == 'off_auto':
                    self.fan_controller.off_auto_mode()
                    pass
                
                elif cmd == 'get_current':
                    data_to_send = {'current': shared_data.datas.get_sensing()}
                    boom = json.JSONEncoder().encode(data_to_send).encode()
                    client_socket.sendall(boom)
                    pass
                
                
                elif cmd == 'get_limit':
                    data_to_send = {'current': shared_data.datas.get_limit()}
                    boom = json.JSONEncoder().encode(data_to_send).encode()
                    client_socket.sendall(boom)
                    pass
                
                
                elif cmd == 'get_safe':
                    data_to_send = {'current': shared_data.datas.get_safe()}
                    boom = json.JSONEncoder().encode(data_to_send).encode()
                    client_socket.sendall(boom)
                    pass
                
                
                elif cmd == 'set_limit':
                    shared_data.datas.set_limit(dict_data['modified_value'])
                    pass
                
                
                elif cmd == 'set_safe':
                    shared_data.datas.set_safe(dict_data['modified_value'])
                    pass
                
                elif cmd == 'get_data':
                    if dict_data['offset']=='today':
                        data_to_send = self.db_controller.get_today(dict_data['datatype'])
                        boom = json.JSONEncoder().encode(data_to_send).encode()
                        client_socket.sendall(boom)
                        pass
                    elif dict_data['offset']=='yesterday':
                        data_to_send = self.db_controller.get_yesterday(dict_data['datatype'])
                        boom = json.JSONEncoder().encode(data_to_send).encode()
                        client_socket.sendall(boom)
                        pass
                    pass
                
                
                elif cmd == 'ok':
                    pass
                
                
                else:
                    print('invalid command')
                    pass
                
                client_socket.close()
            
            except:
                pass
            
            pass # while end
                        
        
        pass # method end
    pass # class end
        
