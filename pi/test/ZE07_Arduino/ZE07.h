#pragma once

#include <SoftwareSerial.h>
#include <arduino.h>
#include <stdint.h>
#include <array>
#include "Timer.h"

//상태 플래그 열거입니다.
enum class StateFlag
{ 
    WAITING, 
    OK 
};

//배열 길이입니다.
constexpr auto MAXLENGTH = 9;

class ZE07CO_Sensor
{
public:
    ZE07CO_Sensor()=delete;
    virtual ~ZE07CO_Sensor()=default;
    ZE07CO_Sensor(const ZE07CO_Sensor&)=delete;
    ZE07CO_Sensor& operator=(const ZE07CO_Sensor&)=delete;
    ZE07CO_Sensor(ZE07CO_Sensor&&)=default;
    ZE07CO_Sensor& operator=(ZE07CO_Sensor&&)=default;

public:
    ZE07CO_Sensor(HardwareSerial* Serial);	//read the uart signal by hardware uart,such as D0
    ZE07CO_Sensor(SoftwareSerial* Serial);	//read the uart signal by software uart,such as D10
    ZE07CO_Sensor(int pin,float ref);			//read the analog signal by analog input
                            // pin ,such as A2; ref:voltage on AREF pin
    bool available(uint16_t timeout);		//new data was recevied
    float uartReadPPM();		//get the concentration(ppm) by uart signal
    float dacReadPPM();		//get the concentration(ppm) by analog signal

private:
    Stream *mySerial;			// 
    using StackType = std::array<uint8_t,MAXLENGTH>;
    StackType receivedCommandStack;
    uint8_t checkSum();
    void boucle();
    bool receivedFlag;
    uint8_t _sensorPin;
    	
    StateFlag _status;
    uint8_t _index = 0;
    float _ref;
};