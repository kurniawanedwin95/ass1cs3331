#!usr/bin/python

#socket implementation
import socket
import pickle
import random
import sys

def readAndResponse(s,message,client):
  if(message['FIN'] == False):
    if(message['SYN'] == True and message['ACK'] == False):
      print 'SYN received'
      # value = {'SYN':True,'ACK':True,'FIN':False,'seq_num':random.randint(0,10000),'ack_num':message['seq_num']+1,'data':''}
      value = {'SYN':True,'ACK':True,'FIN':False,'seq_num':0,'ack_num':message['seq_num']+1,'data':''}
      message = pickle.dumps(value)
      s.sendto(message, client)
      print 'SYN+ACK packet sent'
      message = pickle.loads(message)
    elif(message['SYN'] == False and message['ACK'] == True):
      print 'ACK Received, seq num is', message['seq_num']
      return message['seq_num']
    else:
      print 'Something wrong somewhere'
    
  else:
    #Sends ACK and FIN together, waits for ACK, and closes the program
    if(message['SYN'] == False and message['ACK'] == False):
      print 'FIN received'
      value = {'SYN':False,'ACK':True,'FIN':True,'seq_num':message['ack_num']+1,'ack_num':message['seq_num']+1,'data':''}
      message = pickle.dumps(value)
      s.sendto(message, client)
      print 'ACK+FIN packet sent'
      message, client = s.recvfrom(1024)
      print 'ACK received, terminating connection'
      s.close()
      print 'Connection terminated'
      sys.exit()

def readData(s,expected_seq_num,message,client):
  if(message['SYN'] == True and message['ACK'] == False and message['FIN'] == False):
    
    if(message['seq_num'] == expected_seq_num):
      #ACKed properly
      data = message['data']
      ack_num = message['seq_num']+len(message['data'])
      expected_seq_num = ack_num
      print 'expected next seq num is:',ack_num
      value = {'SYN':False,'ACK':True,'FIN':False,'seq_num':message['ack_num'],'ack_num':ack_num,'data':''}
      message = pickle.dumps(value)
      s.sendto(message, client)
      print 'ACK packet sent'
      return expected_seq_num
    else:
      value = {'SYN':False,'ACK':True,'FIN':False,'seq_num':message['ack_num'],'ack_num':expected_seq_num,'data':''}
      message = pickle.dumps(value)
      s.sendto(message, client)
      print 'Improper ACK, expected seq_num:',expected_seq_num
      return expected_seq_num
  else:
    print 'Something is wrong'
    return expected_seq_num

if __name__ == '__main__':
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  host = '' #local
  receiver_port = int(sys.argv[1])
  s.bind((host, receiver_port))
  print 'server is waiting for UDP connection'
  data = ''
  while 1:
    rec_message, client = s.recvfrom(1024) #buffer size 1kb
    rec_message = pickle.loads(rec_message)
    if rec_message['data'] == '':
      expected_seq_num = readAndResponse(s,rec_message,client)
    else:
      expected_seq_num = readData(s,expected_seq_num,rec_message,client)
  
  