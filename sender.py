#!usr/bin/python

import socket
import sys

#might comment them first, then add as more are implemented
receiver_host_ip = sys.arg[1]
receiver_port = sys.arg[2]
# f = sys.arg[3]
# MWS = sys.arg[4]
# MSS = sys.arg[5]
# timeout = sys.arg[6]
# pdrop = sys.arg[7]
# seed = sys.arg[8]

s = socket.socket(AF_INET, SOCK_DGRAM)
try:
    s.connect((receiver_host_ip, receiver_port))
    s.recv(1024)
    #handshakes
except socket.error:
    print 'Could not connect to server, terminating program.\n'
