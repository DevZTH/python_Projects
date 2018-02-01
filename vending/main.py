import modbus
import online_check
import offline_check
import time





while True:
    time.sleep(0.5)
    passwd = modbus.recive_packet()
    print ("online validation...")
    valid,online = online_check.onlinecheck(passwd)
    #online = False
    if (online == False):
        print ("offline validation...")
        valid=offline_check.offlinecheck(passwd)
    if (valid == True):
        print ("packet valid")
        modbus.send_valid()
    else:
        print ("packet novalid")
        modbus.send_novalid()
        #time.sleep(1)
        #modbus.send_valid()
