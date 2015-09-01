#-*- coding:utf-8 -*-

import socket
import struct
import time
import codecs 
import sys
'''
temp = ('type@=qrl/rid@=50016/')
len_dword = len(temp) + 4*2 +1
message = ''
message += struct.pack('I', len_dword)
message += struct.pack('I', len_dword)
message += struct.pack('I', 689)
'''

def LoginToMainServer(room_id,gid):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('danmu.douyutv.com', 8602))
    temp = ('type@=loginreq/username@=/password@=/roompass@=/roomid@=%s/devid@=231F61BD4964FEDBA49CCA7EEC1807C9/rt@=%d/vk@=24d43a31083d97881b077895d74966fa/ver@=20150826/')
    temp1= temp % (room_id, time.time())
    len_dword = len(temp1) + 4*2 + 1

    message = ''
    message += struct.pack('I', len_dword)
    message += struct.pack('I', len_dword)
    message += struct.pack('I', 689)
    real_temp = message + temp1 + '\x00' 
   # s.send(real_temp)

    tamp1 = ('type@=joingroup/rid@=%s/gid@=%s/')
    tamp2 = tamp1 % (room_id,gid)
    tamp = tamp2
    len_dword1 = len(tamp) + 4*2 +1
    massage = ''
    massage += struct.pack('I', len_dword1)
    massage += struct.pack('I', len_dword1)
    massage += struct.pack('I', 689)
    real_tamp = massage + tamp + '\x00'

    s.send(real_temp)
    data = s.recv(1024)
    print 'data: ',data

    time.sleep(3)

    s.send(real_tamp)
    while True:
    	temp = s.recv(1024)
	if temp[18:29] == 'chatmessage':
		pos1 = temp.find('content@=')
		pos2 = temp.find('/', pos1)
		pos3 = pos1 + len('content@=')
		content = temp[pos3:pos2]

		pos4 = temp.find('snick@=')
		pos5 = temp.find('/', pos4)
		pos6 = pos4 + len('snick@=')
		nickname = temp[pos6:pos5]

		a = nickname+': '+content
		b = a.decode('utf8')
		print b
    s.close()
    
def GetGid(room_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('119.90.49.109',8044))
    temp = ('type@=loginreq/username@=/password@=/roompass@=/roomid@=%s/devid@=231F61BD4964FEDBA49CCA7EEC1807C9/rt@=%d/vk@=24d43a31083d97881b077895d74966fa/ver@=20150826/')
    temp1 = temp % (room_id, time.time())
    len_dword = len(temp1) + 4*2 +1
    
    message = ''
    message += struct.pack('I', len_dword)
    message += struct.pack('I', len_dword)
    message += struct.pack('I', 689)
    real_temp = message + temp1 +'\x00'
    
    s.send(real_temp)

    temp = s.recv(1024)
    print "temp: ", temp
    data = s.recv(1024)
    print "data: ", data

    t_pos1 = temp.find('username@=')
    t_pos2 = temp.find('/', t_pos1)
    t_pos3 = t_pos1 + len('username@=')
    username = temp[t_pos3:t_pos2]

    d_pos1 = data.find('gid@=')
    d_pos2 = data.find('/', d_pos1)
    d_pos3 = d_pos1 + len('gid@=')
    gid = data[d_pos3:d_pos2]
    s.close()
   #print "username: ",username 
    print "gid: ",gid
    return gid

if __name__ == "__main__":
    room_id = raw_input('please input room_id: ')
    gid = GetGid(room_id)
    LoginToMainServer(room_id,gid)


