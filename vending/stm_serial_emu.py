import time, serial
#emulation of vending machine

DEVICE = '/dev/ttyS0'
BAUDRATE = 115200

current_millis = lambda: int(round(time.time() * 10000))

port = serial.Serial(
    port=DEVICE,
    baudrate=BAUDRATE,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
MSG= [0x00,0x10,0x01,0x31,0x30,0x30,0x30,0x31,0x37,0x36,0x36,0x37,0xB9,0xCB]

port.isOpen()
while True:
    time.sleep(1)
    for i in MSG:
        port.write(MSG)

