#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3, time

DBPATH = '/opt/vending/usedkeys.db'

def checkCODE(code):
    COST=4
    crc = code % 1000;

    pass_crc = code - (code % 100000) #pass first 4 gigs
    litres = (code - pass_crc - crc) // 1000 //COST   #second 2digs
    code = code // 1000 *1000
    crc_calc = (13579 ^ litres ^ code) % 1000
    #print(pass_crc)
    #print(litres)
    #print(code)
    #print("stored:" + str(crc) + "caculated:" + str(crc_calc))
    if( int(crc) == int(crc_calc) ):
        return True
    return False

def offlinecheck(code):
    result = checkCODE(code)
    db = sqlite3.connect(DBPATH)
    cursor = db.cursor()
    if(result == True):
        print("code valid")
        cursor.execute("SELECT * FROM `ukeys` WHERE `code` = " + str(code))
        #print( "SELECT * FROM `ukeys` WHERE `code` = " + str(code) )
        row = cursor.fetchone()
        if(row != None):
            print (row)
            code,remain,datatime,sync = row
            cursor.execute("UPDATE `ukeys` SET code = code,remain = 0  WHERE `code` = " + str(code))
            result == False
            print ("code used" )
        else:
            cursor.execute("insert into ukeys values  (?,?,?,?);",
            ( code,"0", int(time.time()),"0" ) )
            db.commit()
            db.close()
    return result
#offlinecheck(12704874)
#checkCODE(12604386)
#checkCODE(104338)