import numpy as np

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
    return crc
    
print (hex(CRC16calc([0x00,0x10,0x01,0x31,0x30,0x30,0x30,0x31,0x37,0x36,0x36,0x37])))
print (hex(CRC16calc([0x10,0x00,0x81,0x00])))