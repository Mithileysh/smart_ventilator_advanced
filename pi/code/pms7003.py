import serial
import platform

S_PORT = "/dev/ttyUSB2"

p_ver = platform.python_version_tuple()[0]

def connect_serial(serial_dev):
    return serial.Serial(serial_dev,
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1.0)

def pms7003(serial_dev):
    try:
        ser = connect_serial(serial_dev)
        while True:
            s=ser.read(32)
            
            if not checksum(s):
                return None

            if p_ver == '2':
                if len(s) >= 4 and s[0] == "\x42" and s[1] == "\x4d":
                    pm1 = ord(s[10])*256 + ord(s[11])
                    pm25 = ord(s[12])*256 + ord(s[13])
                    pm10 = ord(s[14])*256 + ord(s[15])
                    return {'pm1.0': pm1, 'pm2.5': pm25, 'pm10': pm10}
                break
            else:
                if len(s) >= 4 and s[0] == 0x42 and s[1] == 0x4d:
                    pm1 = s[10]*256 + s[11]
                    pm25 = s[12]*256 + s[13]
                    pm10 = s[14]*256 + s[15]
                    return {'pm1.0': pm1, 'pm2.5': pm25, 'pm10': pm10}
                break 
    except:
        traceback.print_exc()
     
def read(serial_dev=S_PORT):
    result = pms7003(serial_dev)
    if result is not None:
        return result

def checksum(array):
    sum = 0
    for e in array:
        sum+=e

    sum -= (array[30] + array[31])
  
    return sum == (array[30]*256 + array[31])


#while True:
#    ss = read()
#    print(ss)