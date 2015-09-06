#!/usr/bin/env python
#-*- coding:utf-8 -*-

import socket
import struct
import time
import codecs
import sys
import douyu_tools

'''
temp = ('type@=qrl/rid@=50016/')
len_dword = len(temp) + 4*2 +1
message = ''
message += struct.pack('I', len_dword)
message += struct.pack('I', len_dword)
message += struct.pack('I', 689)
'''


if __name__ == "__main__":
    room_id = raw_input('please input room_id: ')

    room_info = douyu_tools.getRoomInfo(room_id)
    server = room_info['data']['servers'][0]
    s = douyu_tools.connectMainServer(server['ip'], server['port'], room_id)
    # username = douyu_tools.getUserNameFromMainServer(s)
    gid = douyu_tools.getGidFromMainServer(s)
    s.close()


    s = douyu_tools.connectDanmuServer(8602, room_id)
    data = s.recv(1024)
    # print 'data: ',data

    s = douyu_tools.joinDanmuRoom(s, room_id, gid)

    while True:
        nickname, content = douyu_tools.getOneDanmu(s)
        print nickname, ': ', content
    s.close()
