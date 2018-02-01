#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import MySQLdb

import restjson

def sms_parse(sms,phone_number):
    msg= u"Для получения кода отправте: voda <литры> например: voda 5"
    sms = sms.upper()
    word = sms[:4]
    print (word)
    if(word == "VODA"):
        try:
            litres = int(sms[4:])
            if(litres > 24):
                msg = u"не более 24 литров пожалуйста укажите меньшее число..."
            if(litres < 1):
                msg = u"к сожалению мы не можем налить вам 0 и менее литров"
            else:
                passwd, online = restjson.get_code (phone_number,litres)
                msg = u"ваш код на " + str(litres)
                msg += u" литров : "
                msg += str(passwd)
                msg = unicode(msg)
            return msg
        except:
            msg = u"Для получения кода отправте: voda <литры> например: voda 5"
    return msg


def sms_send(phone_number,sms_text):
    global db

    if sys.version_info.major == 3:
        encoded_sms = ''.join(format(i, '02X') for i in sms_text.encode('utf-16-be'))
    else:
        uni =bytearray( unicode(sms_text).encode('utf-16-be') )
        encoded_sms = ''.join(format(i, '02X') for i in uni)

    sql = "INSERT INTO outbox ( DestinationNumber, Text, CreatorID, Coding, DeliveryReport) VALUES ('" + phone_number + "', '" + encoded_sms + "', 'Program', 'Unicode_No_Compression','no' );"
    print (sql)
    db.query(sql)




db = MySQLdb.connect(host="localhost",
     user="smsd",
     passwd="6n8ff3hd6hg",
     db="smsd", charset='utf8')
#cursor = db.cursor()
#try:
db.query("""SELECT * FROM `inbox` WHERE`Processed` = 'false' """)
#use result
result = db.store_result()

#row = result.fetch_row(how=1)
rows = result.fetch_row(maxrows=0,how=1)
#except _mysql_exceptions e:

for row in rows:
    #print (row)
    print (row["SenderNumber"])
    #print (row["TextDecoded"])
    #print (row["Processed"])
    #print (row["ID"])
    if(row["SenderNumber"] != "MegaFon"):  # banned
        sms_result = sms_parse(row["TextDecoded"], row["SenderNumber"]) # check sms
        sms_send(row["SenderNumber"],sms_result) # send reply
    qte = "UPDATE `inbox` SET `Processed` = 'true' WHERE `inbox`.`ID` = "
    qte = qte + str(row["ID"]) + " ;"
    print (qte)
    db.query(qte) # set used
