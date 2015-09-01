#-*- coding:utf-8 -*-

import socket
import struct
import time

def GetGid():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('119.90.49.109',8042))
    
    temp = ('type@=loginreq/username@=/password@=/roompass@=/roomid@=16789/devid@=231F61BD4964FEDBA49CCA7EEC1807C9/rt@=%d/vk@=24d43a31083d97881b077895d74966fa/ver@=20150826/')
    temp1 = temp % time.time()
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
    print "username: ",username 
    print "gid: ",gid

if __name__ == "__main__":
	GetGid()
