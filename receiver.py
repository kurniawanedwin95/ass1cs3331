#!usr/bin/python

#socket implementation
import socket
import pickle
import sys

def readAndResponse(s,message,client):
  if(message['FIN'] == False):
    if(message['SYN'] == True and message['ACK'] == False):
      print 'SYN received'
      print message
      value = {'SYN':True,'ACK':True,'FIN':False,'seq_num':1,'ack_num':message['seq_num']+1}
      message = pickle.dumps(value)
      s.sendto(message, client)
      print 'SYN+ACK packet sent'
    
    elif(message['SYN'] == False and message['ACK'] == True):
      print 'ACK Received'
      print message
      
    else:
      print 'Something wrong somewhere'
    
  else:
    #Sends ACK and FIN together and closes the program
    if(message['SYN'] == False and message['ACK'] == False):
      print 'FIN received'
      value = {'SYN':False,'ACK':True,'FIN':True,'seq_num':message['ack_num']+1,'ack_num':message['seq_num']+1}
      message = pickle.dumps(value)
      s.sendto(message, client)
      print 'ACK+FIN packet sent'
      s.close()
      print 'Connection terminated'
      sys.exit()
    


if __name__ == '__main__':
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  host = '' #local
  receiver_port = int(sys.argv[1])
  s.bind((host, receiver_port))
  print 'server is waiting for UDP connection'
  
  while 1:
    message, client = s.recvfrom(1024) #buffer size 1kb
    message = pickle.loads(message)
    readAndResponse(s,message,client)

  