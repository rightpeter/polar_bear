import socket
import sys

# Crete a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('danmu.douyutv.com', 8601)
print >> sys.stderr, 'connection to %s port %s' % server_address
sock.connect(server_address)

data = ''
try:
    # Send data
    message = ''
    message += chr(0x5c)
    message += chr(0x00)
    message += chr(0x00)
    message += chr(0x00)
    message += chr(0x5c)
    message += chr(0x00)
    message += chr(0x00)
    message += chr(0x00)
    message += chr(0xb1)
    message += chr(0x02)
    message += chr(0x00)
    message += chr(0x00)
    message += 'type@=loginreq/username@=auto_oaTohTXXvl/password@=1234567890123456/roomid@=216501/.'
    print >> sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    while True:
        tmp = sock.recv(1024)
        print >> sys.stderr, 'tmp: ', tmp
        if not tmp:
            break
        data += tmp

finally:
    print >> sys.stderr, data
    print >> sys.stderr, 'closing socket'
    sock.close()
