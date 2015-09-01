#-*- coding:utf-8 -*-

import socket
import struct
import time

'''
temp = ('type@=qrl/rid@=50016/')
len_dword = len(temp) + 4*2 +1
message = ''
message += struct.pack('I', len_dword)
message += struct.pack('I', len_dword)
message += struct.pack('I', 689)
'''

def LoginToMainServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('danmu.douyutv.com', 8602))

    room_id = 16789
    temp = ('type@=loginreq/username@=/password@=/roompass@=/roomid@=%d/devid@=460303304A21771233BF64E3BC1E5461/rt@=%d/vk@=015c822ad706857355d3e6db18c35cbd/ver@=20150331/')
    temp1= temp % (room_id, time.time())
    len_dword = len(temp1) + 4*2 + 1

    message = ''
    message += struct.pack('I', len_dword)
    message += struct.pack('I', len_dword)
    message += struct.pack('I', 689)
    real_temp = message + temp1 + '\x00' 
   # s.send(real_temp)

    tamp1 = ('type@=joingroup/rid@16789/gid@=55/')
    tamp = tamp1 
    len_dword1 = len(tamp) + 4*2 +1
    massage = ''
    massage += struct.pack('I', len_dword1)
    massage += struct.pack('I', len_dword1)
    massage += struct.pack('I', 689)
    real_tamp = massage + tamp + '\x00'
    s.send(real_temp)
    time.sleep(3)
    s.send(real_tamp)

    data = s.recv(1024)
    print data
    temp = s.recv(1024)
    print temp
    s.close()
	
if __name__ == "__main__":
	LoginToMainServer()
