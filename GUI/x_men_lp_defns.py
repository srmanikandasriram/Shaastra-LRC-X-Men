'''
  All system parameters are defined here.
'''

ROVER_IP_ADDR = '192.168.0.101'
ROVER_CMD_PORT = 8888

CENTRAL_IP = '192.168.0.100'

ROV_WIDTH = 30.5e-02
ROV_WHEEL_DIA = 10.8e-02
ROV_ENC_RES = 30.0

SUBMIT_PART1 = "sshpass -p mani123 scp"
SUBMIT_PART2 = "manikandasriram@" + CENTRAL_IP + ":~/GUI/"

VIDEOFEED_LAUNCH = 'gst-launch udpsrc port=5000 ! smokedec ! autovideosink'
