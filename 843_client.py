import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('danmu.douyutv.com', 843)
print >> sys.stderr, 'connectin to %s port %s' % server_address
sock.connect(server_address)

data = ''
try:
    # Send datat
    message = '<policy-file-request/> .'
    print >> sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    while True:
        tmp = sock.recv(1024)
        if not tmp:
            break
        data += tmp

finally:
    print >> sys.stderr, 'data: ', data
    print >> sys.stderr, 'closing socket'
    sock.close()
