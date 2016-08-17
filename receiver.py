#!usr/bin/python

#will implement in socketserver
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = #something
port = 20000 #somewhere unused and safe

s.bind((host, port))
s.listen(5) #why is this 5?