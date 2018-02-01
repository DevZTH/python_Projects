#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time, serial
import numpy as np


DEVICE = '/dev/ttyS3'
BAUDRATE = 115200

port = serial.Serial(
    port=DEVICE,
    baudrate=BAUDRATE,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

port.isOpen()


PCRC= np.uint16(0xA001)


def CRC16calc(buffer=bytearray([1, 2, 3, 4, 5, 6, 7, 8, 9,10]),crc=np.uint16(0xffff)):
    for i in buffer:
        crc = crc ^ i
        j = 0
        while(j < 8):
            if((crc & 0x0001) != 0x0000):
                crc = (crc >> 1) ^ PCRC
            else:
                crc = crc >> 1
            j += 1
    #swap bytes
    return crc

def wait_packet():
    while True:
        time.sleep(0.05)
        if ( port.inWaiting() > 13):
                ch = port.read(1)
                if(ch == chr(0) ):
                    if(port.read(1) == chr(0x10) ):
                        if(port.read(1) == chr(0x01)):
                            code = bytearray(port.read(9))
                            crc = ord(port.read(1))<<8
                            crc=crc | (ord(port.read(1)))
                            return code, crc




#wait and recive packet from STM
def recive_packet():
    code,packet_crc = wait_packet()#делать подсчет контрольной суммы
    print("recived_code " + code)
    calc_crc = CRC16calc(bytearray(chr(0) + chr(0x10) + chr(0x01) + code))
    print(hex(packet_crc) + " : " + hex(calc_crc))
    try:
        return int(code)
    except:
        return 0
#send novalid reply
def send_novalid():
    MSG = bytearray([0x10,0x00,0x81,0x00,0xB4,0x64]) #пароль не верный
    for i in MSG:
        port.write(chr(i))
#sen valid reply
def send_valid():
    MSG = bytearray([0x10,0x00,0x81,0x01,0x74,0xA5]) #пароль верный
    for i in MSG:
        #print(hex(i))
        port.write(chr(i))
 #0x10,0x00,0x81,0x01,0x74,0xA5

 #0x10,0x00,0x81,0x01,0x74,0xA5


#code =recive_packet()
#print code