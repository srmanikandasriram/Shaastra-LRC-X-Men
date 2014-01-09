'''
  All system parameters are defined here.
'''

ROVER_IP_ADDR = '127.0.0.1'
ROVER_CMD_PORT = 8888

VIDEOFEED_LAUNCH = 'gst-launch udpsrc port=5000 ! smokedec ! xvimagesink'
