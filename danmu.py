#!/usr/bin/env python
# -*- coding:utf-8 -*-

import douyu_tools
import random
import time

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
    index = random.randint(0, 9)
    print 'index: ', index
    server = room_info['data']['servers'][index]
    s = douyu_tools.connectMainServer(server['ip'], server['port'], room_id)
    # username = douyu_tools.getUserNameFromMainServer(s)
    data = s.recv(1024)
    print 'unkown data: ', data
    data = s.recv(1024)
    s.close()
    print 'receiveGid data: ', data
    gid, = douyu_tools.getGidFromMainServer(data)
    print 'gid: ', gid

    s = douyu_tools.connectDanmuServer(8602, room_id)
    data = s.recv(1024)
    print 'data: ', data

    s = douyu_tools.sendKeepLive(s)
    data = s.recv(1024)
    print 'sendKeepLive: ', data

    s = douyu_tools.joinDanmuRoom(s, room_id, gid)
    # data = s.recv(1024)
    # print 'joinDanmuRoom: ', data

    last_keep_alive_time = int(time.time())
    while True:
        data = s.recv(1024)
        last_keep_alive_time = douyu_tools.checkKeepLive(s, last_keep_alive_time)
        data_list = douyu_tools.getDataList(data)
        # print 'len(data_list): ', len(data_list)
        for data in data_list:
            danmu_type, = douyu_tools.getDanmuType(data)
            print '--------type: ', danmu_type
            if danmu_type == douyu_tools.TYPE_DANMU:
                print '[DANMU]data: ', data
                content, snick = douyu_tools.getDanmuDetails(data)
                print snick, ': ', content
            elif danmu_type == douyu_tools.TYPE_YUWAN:
                print '[YUWAN]data: ', data
                hits, snick = douyu_tools.getYuwanDetails(data)
                print snick, '赠送了100鱼丸', hits, '连击'
            elif danmu_type == douyu_tools.TYPE_DONA_YUWAN:
                print '[YUWAN DONA]data: ', data
                hc, snick = douyu_tools.getDonaYuwanDetails(data)
                print snick, '赠送了100鱼丸', hc, '连击'
            elif danmu_type == douyu_tools.TYPE_USER_ENTER:
                print '[USER_ENTER]data: ', data
                snick, deserve_lev, scq_cnt = douyu_tools.getUserEnterDetails(data)
                print 'LV', deserve_lev, ' * ', scq_cnt, ' ', snick, '来到本房间'
            elif danmu_type == douyu_tools.TYPE_ONLINE_GIFT:
                print '[ONLINE_GIFT]data: ', data
                sil, nn = douyu_tools.getOnlineGiftDetails(data)
                print nn, '领取了', sil, '个鱼丸'
            elif danmu_type == douyu_tools.TYPE_BLACK_RES:
                print '[BLACK_RES]data: ', data
                dnick, = douyu_tools.getBlackResDetails(data)
                print dnick, '被禁言'
            elif danmu_type == douyu_tools.TYPE_BUY_DESERVE:
                print '[BUY_DESERVE]data: ', data, ' type: ', danmu_type
                lev, hits, snick = douyu_tools.getBuyDeserveDetails(data)
                print snick, '购买了', lev, '级酬勤 x', hits, '连击'
            elif danmu_type == douyu_tools.TYPE_KEEP_LIVE:
                print '[KEEP_ALIVE]data: ', data
            else:
                print 'Error: ', data
    s.close
