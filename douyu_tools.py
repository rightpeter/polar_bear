#!usr/bin/env python
#-*-coding:utf-8-*-
import json
import urllib
import socket
import time
import struct

DOUYU_API_URL = 'http://api.douyutv.com/api/client/room/'
DOUYU_DANMU_URL = 'danmu.douyutv.com'
DOUYU_SERVER_LOGIN_REQ = 'type@=loginreq/username@=/password@=/roompass@=/roomid@=%s/devid@=231F61BD4964FEDBA49CCA7EEC1807C9/rt@=%d/vk@=24d43a31083d97881b077895d74966fa/ver@=20150826/'
DOUYU_JOIN_DANMU_ROOM_REQ ='type@=joingroup/rid@=%s/gid@=%s/'
DOUYU_TCP_SEND_SIGN = '\xb1\x02\x00\x00'
DOUYU_TCP_RECV_SIGN = '\xb2\x02\x00\x00'


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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((url, int(port)))
    req_str = DOUYU_SERVER_LOGIN_REQ % (room_id, time.time())
    data = packString(req_str)

    s.send(data)
    return s


def getUserNameFromMainServer(s):
    data = s.recv(1024)
    pos1 = temp.find('username@=')
    pos2 = temp.find('/', pos1)
    pos1 = pos1 + len('username@=')
    username = temp[pos1:pos2]
    return username


def getGidFromMainServer(s):
    data = s.recv(1024)
    pos1 = data.find('gid@=')
    pos2 = data.find('/', pos1)
    pos1 = pos1 + len('gid@=')
    gid = data[pos1:pos2]
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


def getOneDanmu(s):
    data = s.recv(1024)
    if data[18:29] == 'chatmessage':
        pos1 = data.find('content@=')
        pos2 = data.find('/', pos1)
        pos1 = pos1 + len('content@=')
        content = data[pos1:pos2]

        pos1 = data.find('snick@=')
        pos2 = data.find('/', pos1)
        pos1 = pos1 + len('snick@=')
        nickname = data[pos1:pos2]

        return nickname.decode('utf8'), content.decode('utf8')
    else:
        return '', ''


def main():
	rid = raw_input("Please input room id:")
	data = get_room_info(rid)
	if data['error'] != 0:
		raise Exception("GET_JSON_ERROR")
	data_string = json.dumps(data,sort_keys=True,indent=2)
	print data_string

if __name__ == "__main__":
	main()
