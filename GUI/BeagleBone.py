'''
  Team X-Men from IIT Madras for Shaastra 2014 Lunar Rover Challenge
  This Python script uses Socket module available in Python to establish
  communication with the Control Center and receive commands and send data.
'''

import socket
import sys
import pickle
import subprocess

from x_men_rv_defns import *


encoders_count = {
  ENCL1_PIN : 0,
  ENCR1_PIN : 0,
  }

# ISR for Encoders  
def handle_encoder(x):
    global encoders_count
    encoders_count[x] += 1
    print encoders_count[x]


HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

def send_encoders_data(arg):
    encoders_count_cpy = encoders_count
    encoders_count.update({k : 0 for k in encoders_count.iterkeys()}) # reset values to 0
    return encoder_counts_cpy

def take_image(arg):
    #bashCommand = './takeimage.sh'    # Construct bashCommand from arg
    #subprocess.call([bashCommand],shell=True)
    return 'Take images'

def take_video(arg):
    return 'Take videos'

def default(arg):
    return 'Default actions'

def begin_videofeed(arg):
    bashCommand = './videofeed.sh'
    pid = subprocess.Popen("gst-launch videotestsrc ! ffmpegcolorspace ! smokeenc ! udpsink host=127.0.0.1 port=5000",shell=True).pid    # Command to spawn independant process
    print 'Process ID ' + str(pid)
    return 'Video transmission successfully begun'

def drive(arg):
    return 

handleCmd = {
    'enc' : send_encoders_data,
    'img' : take_image,
    'vid' : take_video,
    'vds' : begin_videofeed,
    'drv' : drive,
    }

while 1:
    # receive data from client (data, addr)
    data,addr = s.recvfrom(1024)

    if not data: 
        break
    
    cmd,arg = pickle.loads(data)
    
    if cmd in handleCmd:
        reply = handleCmd[cmd](arg)
    else:
        reply = default(arg)
    
    s.sendto(pickle.dumps(reply) , addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + str(type(reply)) + ' :: ' + str(reply)

GPIO.cleanup()
s.close()
