#!usr/bin/env python
# -*-coding:utf-8-*-
import json
import urllib
import socket
import time
import struct
import re

TYPE_DANMU = 'chatmessage'
TYPE_YUWAN = 'dgn'
TYPE_DONA_YUWAN = 'donateres'
TYPE_USER_ENTER = 'userenter'
TYPE_ONLINE_GIFT = 'onlinegift'
TYPE_BLACK_RES = 'blackres'
TYPE_BUY_DESERVE = 'bc_buy_deserve'
TYPE_KEEP_LIVE = 'keeplive'

DOUYU_API_URL = 'http://api.douyutv.com/api/client/room/'
DOUYU_DANMU_URL = 'danmu.douyutv.com'
DOUYU_SERVER_LOGIN_REQ = 'type@=loginreq/username@=/password@=/roompass@=/roomid@=%s/devid@=231F61BD4964FEDBA49CCA7EEC1807C9/rt@=%d/vk@=24d43a31083d97881b077895d74966fa/ver@=20150909/'
DOUYU_JOIN_DANMU_ROOM_REQ = 'type@=joingroup/rid@=%s/gid@=%s/'
DOUYU_KEEP_ALIVE = 'type@=keeplive/tick@=%s/'
DOUYU_TCP_SEND_SIGN = '\xb1\x02\x00\x00'
DOUYU_TCP_RECV_SIGN = '\xb2\x02\x00\x00'

REG_TYPE = re.compile(r'type@=([^/]*)/')
REG_CONTENT = re.compile(r'content@=([^/]*)/')
REG_SNICK = re.compile(r'snick@=([^/]*)/')
REG_SRC_NCNM = re.compile(r'src_ncnm@=([^/]*)/')
REG_SNICKA = re.compile(r'Snick@A=([^@]*)@')
REG_USERNAME = re.compile(r'username@=([^/]*)/')
REG_GID = re.compile(r'gid@=([^/]*)/')
REG_HITS = re.compile(r'hits@=([^/]*)/')
REG_YUWAN_HC = re.compile(r'hc@=([^/]*)/')
REG_DESERVE_LEV = re.compile(r'Sm_deserve_lev@A=([^@]*)@')
REG_SCQ_CNT = re.compile(r'Scq_cnt@A=([^@]*)@')
REG_SIL = re.compile(r'sil@=([0-9]*)/')
REG_NN = re.compile(r'nn@=([^/]*)/')
REG_DNICK = re.compile(r'dnick@=([^/]*)/')
REG_LEV = re.compile(r'lev@=([0-9]*)/')
REG_GFID = re.compile(r'gfid@=([0-9]*)/')


def getJson(url):
    page = urllib.urlopen(url)
    get_json = page.read()
    data = json.loads(get_json)
    return data


def getRoomInfo(room_id):
    url = DOUYU_API_URL + room_id
    data = getJson(url)
    return data


def reGetDetails(re_list, data):
    ret = []

    for tre in re_list:
        re_detail = re.findall(tre, data)

        if len(re_detail) > 0:
            detail = re_detail[0]
        else:
            detail = ''

        ret.append(detail)

    return tuple(ret)


def packString(req_str):
    req_len = len(req_str) + 4 * 2 + 1

    data = ''
    data += struct.pack('I', req_len)
    data += struct.pack('I', req_len)
    data += DOUYU_TCP_SEND_SIGN
    data = data + req_str + '\x00'

    return data


def connectMainServer(url, port, room_id):
    print 'ConnectMainServer ip: ', url, ' port: ', port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, int(port)))
    req_str = DOUYU_SERVER_LOGIN_REQ % (room_id, time.time())
    print 'connectMainServer req_str: ', req_str
    data = packString(req_str)

    s.send(data)
    return s


def getUserNameFromMainServer(data):
    '''
        return username
    '''
    return reGetDetails([REG_USERNAME], data)


def getGidFromMainServer(data):
    '''
        return gid
    '''
    return reGetDetails([REG_GID], data)


def connectDanmuServer(port, room_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((DOUYU_DANMU_URL, int(port)))
    req_str = DOUYU_SERVER_LOGIN_REQ % (room_id, time.time())
    data = packString(req_str)

    s.send(data)
    return s


def joinDanmuRoom(s, room_id, gid):
    req_str = DOUYU_JOIN_DANMU_ROOM_REQ % (room_id, gid)
    data = packString(req_str)

    s.send(data)
    return s


def sendKeepLive(s):
    req_str = DOUYU_KEEP_ALIVE % (int(time.time()))
    data = packString(req_str)

    # print '[sendKeepLive]data: ', data
    s.send(data)
    return s


def checkKeepLive(s, last_keep_alive_time):
    now = int(time.time())
    if now - last_keep_alive_time > 5:
        s = sendKeepLive(s)
        return now

    return last_keep_alive_time


def getDataList(data):
    # print 'data: ', data
    # tmp_data = data
    data_list = []

    while data:
        req_len = struct.unpack('I', data[0:4])[0]
        print 'req_len: ', req_len, ' data_len: ', len(data)
        data_content = data[12:4 + req_len]
        data = data[4 + req_len:]
        data_list.append(data_content)

    # if len(data_list) > 1:
    #     print '--------------------multi data---------------------'
    #     print '--------------------multi data---------------------'
    #     print 'tmp_data: ', tmp_data
    #     print '--------------------multi data---------------------'
    #     print '--------------------multi data---------------------'
    #     for data in data_list:
    #         print 'data: ', data

    return data_list


def getDanmuType(data):
    '''
        return danmu_type
    '''
    return reGetDetails([REG_TYPE], data)


def getDanmuDetails(data):
    '''
        return content, snick
    '''
    content, snick, gfid = reGetDetails([REG_CONTENT, REG_SNICK, REG_GFID], data)
    if gfid == '50':
        gift = '100鱼丸'
    elif gfid == '51':
        gift = '赞'
    return (content, snick, gift)


def getYuwanDetails(data):
    '''
        return hits, snick
    '''
    hits, src_ncnm, gfid = reGetDetails([REG_HITS, REG_SRC_NCNM, REG_GFID], data)
    if gfid == '50':
        gift = '100鱼丸'
    elif gfid == '51':
        gift = '赞'
    return (hits, src_ncnm, gift)


def getDonaYuwanDetails(data):
    '''
        return hc, snick
    '''
    return reGetDetails([REG_YUWAN_HC, REG_SNICKA], data)


def getUserEnterDetails(data):
    '''
        return snick, deserve_lev, scq_cnt
    '''
    return reGetDetails([REG_SNICKA, REG_DESERVE_LEV, REG_SCQ_CNT], data)


def getOnlineGiftDetails(data):
    '''
        return sil, nn
    '''
    return reGetDetails([REG_SIL, REG_NN], data)


def getBlackResDetails(data):
    '''
        return dnick
    '''
    return reGetDetails([REG_DNICK], data)


def getBuyDeserveDetails(data):
    '''
        return lev, hits, snick
    '''
    return reGetDetails([REG_LEV, REG_HITS, REG_SNICKA], data)
