import serial


S_PORT = "/dev/ttyUSB0"


class Ze07UartReader:
    def __init__(self):
        self.m_serial = serial.Serial(S_PORT, 9600)
        self.m_stack = []
        
        
    # private method. dont use it
    # return true if checksum byte equals other values sum
    def _check_sum(self, right_sum):
        values_sum = 0
        for e in self.m_stack:
            values_sum +=  int(e.hex(),16)
            
        values_sum = (~values_sum + 1)
            
        return values_sum == int(right_sum.hex(), 16)
    
    
    def read(self):
        while True:
            if b'\xff' == self.m_serial.read():
                self.m_stack.append(b'\xff')
                
                if b'\x17' != self.m_serial.read():
                    continue

                # index 1
                self.m_stack.append(b'\0x17')
                
                if b'\x04' != self.m_serial.read():
                    continue
                
                # index 2
                self.m_stack.append(b'\0x04')
                
                # index 3
                self.m_stack.append(self.m_serial.read())
                
                # index 4 # high
                self.m_stack.append(self.m_serial.read())
                
                # index 5 # low
                self.m_stack.append(self.m_serial.read())
                
                # index 6
                self.m_stack.append(self.m_serial.read())
                
                # index 7
                self.m_stack.append(self.m_serial.read())
                
                # index 8 (check sum)
                right_sum = self.m_serial.read()
                if not self._check_sum(right_sum):
                    #return None 
                    pass
                    
                #print('high:{}, low:{}'.format(self.m_stack[4], self.m_stack[5]))
                high = int(self.m_stack[4].hex(), 16)
                low = int(self.m_stack[5].hex(), 16)
                ppm = (high*256 + low) * 0.001
                #print('integer: {} ppm'.format(ppm))
                
                self.m_stack = []
                
                return ppm;
    
    
reader = Ze07UartReader()
    
def read():
    return reader.read()
