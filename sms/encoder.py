import binascii

#''.join(format(i, '02X') for i in s.encode('utf-16-be'))

binascii.hexlify('Привет!!!'.decode('cp866').encode('utf-16-be'))