#!usr/bin/env python
#-*-coding:utf-8-*-
import json
import urllib
import socket
import time
import struct
import re

TYPE_DANMU = 'chatmessage'
TYPE_YUWAN = 'dgn'

DOUYU_API_URL = 'http://api.douyutv.com/api/client/room/'
DOUYU_DANMU_URL = 'danmu.douyutv.com'
DOUYU_SERVER_LOGIN_REQ = 'type@=loginreq/username@=/password@=/roompass@=/roomid@=%s/devid@=231F61BD4964FEDBA49CCA7EEC1807C9/rt@=%d/vk@=24d43a31083d97881b077895d74966fa/ver@=20150831/'
DOUYU_JOIN_DANMU_ROOM_REQ ='type@=joingroup/rid@=%s/gid@=%s/'
DOUYU_TCP_SEND_SIGN = '\xb1\x02\x00\x00'
DOUYU_TCP_RECV_SIGN = '\xb2\x02\x00\x00'

REG_TYPE = re.compile(r'type@=([^/]*)/')
REG_CONTENT = re.compile(r'content@=([^/]*)/')
REG_SNICK = re.compile(r'snick@=([^/]*)/')
REG_SNICK_DONA = re.compile(r'src_ncnm@=([^/]*)/')
REG_USERNAME = re.compile(r'username@=([^/]*)/')
REG_GID = re.compile(r'gid@=([^/]*)/')
REG_YUWAN_HITS = re.compile(r'hits@=([^/]*)/')

def getJson(url):
	page = urllib.urlopen(url)
	get_json = page.read()
	data = json.loads(get_json)
	return data


def getRoomInfo(room_id):
	url = DOUYU_API_URL + room_id
	data = getJson(url)
	return data


def packString(req_str):
    req_len = len(req_str) + 4*2 + 1

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
    username_list = re.findall(REG_USERNAME, data)
    if len(username_list) > 0:
        username = username_list[0]
    else:
        username = ''

    return username


def getGidFromMainServer(data):
    gid_list = re.findall(REG_GID, data)
    if len(gid_list) > 0:
        gid = gid_list[0]
    else:
        gid = 0

    return gid


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


def getDanmuType(data):
    type_list = re.findall(REG_TYPE, data)
    if len(type_list) > 0:
        danmu_type = type_list[0]
    else:
        danmu_type = ''
    return danmu_type


def getDanmuDetails(data):
    content_list = re.findall(REG_CONTENT, data)

    if len(content_list) > 0:
        content = content_list[0].decode('utf-8')
    else:
        content = ''

    snick_list = re.findall(REG_SNICK, data)

    if len(snick_list) > 0:
        snick = snick_list[0].decode('utf-8')
    else:
        snick = ''

    return snick, content


def getYuwanDetails(data):
    yuwan_hits = re.findall(REG_YUWAN_HITS, data)

    if len(yuwan_hits) > 0:
        hits = yuwan_hits[0]
    else:
        hits = 0

    snick_list = re.findall(REG_SNICK_DONA, data)

    if len(snick_list) > 0:
        snick = snick_list[0].decode('utf-8')
    else:
        snick = ''

    return snick, hits

if __name__ == "__main__":
	main()

