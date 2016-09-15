#!usr/bin/python
#python receiver.py 20000 file.txt - command for easy debugging
#socket implementation
import socket
import pickle
import random
import sys

def readAndResponse(f,f2,s,message,client):
  if(message['FIN'] == False):
    if(message['SYN'] == True and message['ACK'] == False):
      print 'SYN received'
      value = {'SYN':True,'ACK':True,'FIN':False,'seq_num':random.randint(0,10000),'ack_num':message['seq_num']+1,'data':''}
      message = pickle.dumps(value)
      s.sendto(message, client)
      print 'SYN+ACK packet sent'
      message = pickle.loads(message)
    elif(message['SYN'] == False and message['ACK'] == True):
      print 'ACK Received'
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
      message = pickle.loads(message)
      print 'ACK received, terminating connection'
      #print log----------------------------------------
      datasize = 'Amount of data received: '+str(totalData)+' bytes\n'
      segmentnum = 'Number of data segmentes received: '+str(totalSegment)+'\n'
      duplicatenum = 'Number of duplicate segments received: '+str(totalDuplicate)+'\n'
      f2.write(datasize)
      f2.write(segmentnum)
      f2.write(duplicatenum)
      #-------------------------------------------------
      s.close()
      f.close()
      f2.close()
      print 'Connection terminated'
      sys.exit()

def readData(f,s,expected_seq_num,dataBuffer,message,client):
  if(message['SYN'] == True and message['ACK'] == False and message['FIN'] == False):
    if(message['seq_num'] == expected_seq_num):
      #ACKed properly
      data = message['data']
      global totalSegment
      global totalData
      totalSegment += 1
      #Reads from buffer if data exists in buffer
      if(dataBuffer.get(message['seq_num']) == None):
        f.write(data)
        ack_num = message['seq_num']+len(message['data'])
        totalData += len(message['data'])
        expected_seq_num = ack_num
      else:
        while (dataBuffer.get(expected_seq_num)!=None):
          global totalDuplicate
          totalDuplicate += 1
          string = dataBuffer.pop(expected_seq_num,None)
          f.write(string)
          totalData += len(string)
          expected_seq_num += len(string)
          ack_num = expected_seq_num
      
      value = {'SYN':False,'ACK':True,'FIN':False,'seq_num':message['ack_num'],'ack_num':ack_num,'data':''}
      message = pickle.dumps(value)
      s.sendto(message, client)
      return dataBuffer,expected_seq_num
      
    else:
      #Improper packet
      dataBuffer[message['seq_num']] = message['data']
      value = {'SYN':False,'ACK':True,'FIN':False,'seq_num':message['ack_num'],'ack_num':expected_seq_num,'data':''}
      message = pickle.dumps(value)
      s.sendto(message, client)
      return dataBuffer,expected_seq_num
  else:
    print 'Something is wrong'
    return dataBuffer,expected_seq_num

if __name__ == '__main__':
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  host = '' #local
  receiver_port = int(sys.argv[1])
  filename = sys.argv[2]
  s.bind((host, receiver_port))
  print 'server is waiting for UDP connection'
  dataBuffer = {}
  totalData = 0
  totalSegment = 0
  totalDuplicate = 0
  
  f = open(filename,'w')#cleans file of previous content
  f.close()
  f = open(filename,'a')
  f2 = open('Receiver_log.txt','w')#cleans file of previous content
  f2.close()
  f2 = open('Receiver_log.txt','a')
  while 1:
    rec_message, client = s.recvfrom(1024) #buffer size 1kb
    rec_message = pickle.loads(rec_message)
    if rec_message['data'] == '':
      expected_seq_num = readAndResponse(f,f2,s,rec_message,client)
    else:
      dataBuffer,expected_seq_num = readData(f,s,expected_seq_num,dataBuffer,rec_message,client)
  
  