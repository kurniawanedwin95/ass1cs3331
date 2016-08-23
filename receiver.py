#!usr/bin/python
#As I don't know whether SocketServer is able to do the assignment or not,
#currently both options will be served.

#socketserver implementation
import SocketServer
import sys

class UDPHandler(SocketServer.BaseRequestHandler):

def handle(self):
    data = self.request[0].strip()
    s = self.request[1]
    print '{} wrote:'.format(self.client_address[0])
    print data
    s.sendto(data.upper(), self.client_address)

if __name__ == "__main__":
    receiver_host_ip = #something
    receiver_port = sys.arg[1]
    server = SocketServer.UDPServer((receiver_host_ip, receiver_port))
    server.serve_forever()

#socket implementation
import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '' #local
receiver_port = sys.arg[1]

s.bind((host, port))
print 'server is waiting for UDP connection'
while 1:
  message, client = s.recvfrom(2048)
  ACK = #something
  s.sendto(ACK, client)