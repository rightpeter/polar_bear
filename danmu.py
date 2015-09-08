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
len_dword = len(temp) + 4*2 + 1
message = ''
message += struct.pack('I', len_dword)
message += struct.pack('I', len_dword)
message += struct.pack('I', 689)
'''


if __name__ == "__main__":
    room_id = raw_input('please input room_id: ')

    room_info = douyu_tools.getRoomInfo(room_id)
    room_id = str(room_info['data']['room_id'])
    print room_id
    server = room_info['data']['servers'][-1]
    s = douyu_tools.connectMainServer(server['ip'], server['port'], room_id)
    # username = douyu_tools.getUserNameFromMainServer(s)
    data = s.recv(1024)
    # print 'login req data 1: ', data
    data = s.recv(1024)
    # print 'login req data 2: ', data
    s.close()
    gid = douyu_tools.getGidFromMainServer(data)
    print 'gid: ', gid


    s = douyu_tools.connectDanmuServer(8602, room_id)
    data = s.recv(1024)
    print 'data: ',data

    s = douyu_tools.joinDanmuRoom(s, room_id, gid)

    while True:
        data = s.recv(1024)
        data_list = douyu_tools.getDataList(data)
        for data in data_list:
        	danmu_type = douyu_tools.getDanmuType(data)
        	if danmu_type == douyu_tools.TYPE_DANMU:
        	    snick, content = douyu_tools.getDanmuDetails(data)
        	    print snick, ': ', content
        	elif danmu_type == douyu_tools.TYPE_YUWAN:
        	    snick, hits = douyu_tools.getYuwanDetails(data)
        	    print snick, '赠送了100鱼丸', hits,'连击'
        	elif danmu_type == douyu_tools.TYPE_DONA_YUWAN:
         	    snick, hc = douyu_tools.getDonaYuwanDetails(data)
        	    print snick, '赠送了100鱼丸', hc,'连击' 
        	else:
        	    print 'Error: ', data
    s.close
