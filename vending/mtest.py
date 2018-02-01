import time, serial
import numpy as np
# TRASH

DEVICE = '/dev/ttyUSB0'
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


def CRC16calc(buffer=bytearray([1, 2, 3, 4, 5, 6, 7, 8, 9,10]),crc=np.uint16(0)):
    for i in buffer:
        crc = crc ^ i
        j = 0
        while(j < 8):
            if((crc & 0x0001) != 0x0000):
                crc = (crc >> 1) ^ PCRC
            else:
                crc = crc >> 1
            j += 1
    return crc

def wait_packet():
    while True:
        time.sleep(0.1)
        print("wait..."+hex(port.inWaiting()) )
        if ( port.inWaiting() > 13):
                ch = port.read(1)
                print("ch" + ch )
                if(ch == chr(0) ):
                    print("valid start")
                    if(port.read(1) == chr(0x10) ):
                        print("valid addr")
                        if(port.read(1) == chr(0x01)):
                            print("valid c")
                            code = bytearray(port.read(9))
                            crc = ord(port.read(1))
                            crc=crc +(ord(port.read(1))<<8)
                            return code, crc

def recive_packet():
    code,packet_crc = wait_packet()
    calc_crc = CRC16calc(bytearray(chr(0)+chr(0x10)+chr(0x01)+code+chr(0) ),0)
    print(hex(packet_crc)+" : "+hex(calc_crc))

recive_packet()