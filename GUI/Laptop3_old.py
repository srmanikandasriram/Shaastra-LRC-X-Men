#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Team X-Men from IIT Madras.
Control Console for Shaastra Lunar Rover Challenge 2014
"""

import sys
import os
import socket
import pickle
import subprocess
import time
import commands
import gtk.gdk
import math
import random
import sys
from PyQt4 import Qt
import signal

from PyQt4 import QtGui, QtCore
from x_men_lp_defns import *               # Import definitions for Laptop
from x_men_rv_defns import *               # Import definitions for Laptop
from time import gmtime, strftime

class Comms():
    def __init__(self):
        # create dgram udp socket
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print 'Failed to create socket. Terminating.'
            sys.exit()
        
        self.host = ROVER_IP_ADDR
        self.port = ROVER_CMD_PORT

    def sendMsg(self,msg):
        try :
            self.sock.sendto(pickle.dumps(msg), (self.host, self.port))
         
            # receive data from client (data, addr)
            data,addr = self.sock.recvfrom(1024)
            reply = pickle.loads(data)
     
        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        return reply
        
    def sendCmd(self,msg):
        try :
            self.sock.sendto(pickle.dumps(msg), (self.host, self.port))     
        except socket.error, msg:
            print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()

paths_video = ['output.raw']
paths_image = ['test.ppm']

class Console(QtGui.QWidget):
    def __init__(self):
        super(Console, self).__init__()
        self.BBB = Comms()
        self.initUI()

    def onFileSystemChangedVideo(self,path):
        """
        Callback when file or folder change
        @param path : Changed path
        @type  path : string
        """
#        subprocess.Popen(["ffmpeg -y -i output.raw -vf \"movie='image_overlay.png' [logo], [in]drawtext=fontfile=/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf:box=1:boxcolor=black@0.3:text='%T':fontsize=30:fontcolor=white:x=100:y=100,[logo] overlay=0:0 [out]\" -r 30 out.mp4"],shell=True)
#        subprocess.Popen(["ffmpeg -y -f h264 -i output.raw -vcodec copy output.mp4 && " + SUBMIT_PART1 + " output.mp4 " + SUBMIT_PART2],shell=True)
#        self.qfsw_video.addPaths(paths_video)
#        QtCore.QObject.connect(self.qfsw_video,QtCore.SIGNAL("directoryChanged(QString)"),self.onFileSystemChangedVideo)
#        QtCore.QObject.connect(self.qfsw_video,QtCore.SIGNAL("fileChanged(QString)"),self.onFileSystemChangedVideo)

    def onFileSystemChangedImage(self,path):
        """
        Callback when file or folder change
        @param path : Changed path
        @type  path : string
        """
#        subprocess.Popen(["ffmpeg -y -i output.raw -vf \"movie='image_overlay.png' [logo], [in]drawtext=fontfile=/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf:box=1:boxcolor=black@0.3:text='%T':fontsize=30:fontcolor=white:x=100:y=100,[logo] overlay=0:0 [out]\" -r 30 out.mp4"],shell=True)
#        subprocess.Popen([SUBMIT_PART1 + " test.ppm " + SUBMIT_PART2],shell=True)
#        self.qfsw_image.addPaths(paths_image)
#        QtCore.QObject.connect(self.qfsw_image,QtCore.SIGNAL("directoryChanged(QString)"),self.onFileSystemChangedImage)
#        QtCore.QObject.connect(self.qfsw_image,QtCore.SIGNAL("fileChanged(QString)"),self.onFileSystemChangedImage)

    def updateDistance(self,reply):
        if str(type(reply))=="<type 'dict'>":
            self.total_enc_cnt['left'] = reply[ENCL1_PIN]
            self.total_enc_cnt['right'] = reply[ENCR1_PIN]
            self.distance['left'] = self.total_enc_cnt['left']/ROV_ENC_RES*ROV_WHEEL_DIA*math.pi
            self.distance['right'] = self.total_enc_cnt['right']/ROV_ENC_RES*ROV_WHEEL_DIA*math.pi
            self.distance_travelled = (self.distance['left'] + self.distance['right']) / 2.0
        else:
            print "hello"

    def initUI(self):
        self.f = open('values.txt','a')
        self.total_enc_cnt = {'left':0,'right':0,}
        self.distance = {'left':0,'right':0,}
        self.distance_travelled = 0
#        self.qfsw_video = QtCore.QFileSystemWatcher(self)
#        self.qfsw_video.addPaths(paths_video)
#        QtCore.QObject.connect(self.qfsw_video,QtCore.SIGNAL("directoryChanged(QString)"),self.onFileSystemChangedVideo)
#        QtCore.QObject.connect(self.qfsw_video,QtCore.SIGNAL("fileChanged(QString)"),self.onFileSystemChangedVideo)
#        signal.signal(signal.SIGINT, signal.SIG_DFL)

#        self.qfsw_image = QtCore.QFileSystemWatcher(self)
#        self.qfsw_image.addPaths(paths_image)
#        QtCore.QObject.connect(self.qfsw_image,QtCore.SIGNAL("directoryChanged(QString)"),self.onFileSystemChangedImage)
#        QtCore.QObject.connect(self.qfsw_image,QtCore.SIGNAL("fileChanged(QString)"),self.onFileSystemChangedImage)
#        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.setGeometry(10, 10, 1500, 900)
        self.setWindowTitle('Control Center | Team X-Men, IIT Madras')
        self.setWindowIcon(QtGui.QIcon('google.png'))
    
        self.col = QtGui.QColor(0, 0, 0)
        self.square = QtGui.QFrame(self)
        self.square.setGeometry(0, 0, 1500, 900)
        self.square.setStyleSheet("QWidget { background-color: %s }" %  self.col.name())
        
        self.background_pic = QtGui.QLabel(self)
        self.background_pic.setGeometry(0, 0, 1366,768)
        self.background_pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/Background2.jpg"))

        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.setToolTip('This is the control panel of <b>Team X-Men</b> for <b>LRC 2014</b>.')

        subprocess.Popen([VIDEOFEED_LAUNCH],shell=True)
        break_loop = 0
        while 1:
            lines = commands.getoutput("wmctrl -l").split("\n")
            for line in lines:
                line = line.replace("  ", " ")
                win = tuple(line.split(" ", 3))
                if 'gst-launch-0.10' in win[3]:
                    break_loop = 1;
            if break_loop == 1:
                break
            else:
                print "gst-launch not yet opened"

        subprocess.Popen(["wmctrl -r gst-launch-0.10 -T \"Team X-men - Live Feed\""],shell=True)
        subprocess.Popen(["wmctrl -r 'Team X-men - Live Feed' -e 0,15,84,640,480"],shell=True)
        subprocess.Popen(["wmctrl -r 'Team X-men - Live Feed' -b toggle,above"],shell=True)
        
        w = gtk.gdk.window_foreign_new( gtk.gdk.get_default_root_window().property_get("_NET_ACTIVE_WINDOW")[2][0] )
        w.set_decorations( (w.get_decorations()+1)%2 ) # toggle between 0 and 1
        gtk.gdk.window_process_all_updates()
        gtk.gdk.flush()
        subprocess.Popen(["wmctrl -a 'Control Center | Team X-Men, IIT Madras'"],shell=True)
        
#        self.title = QtGui.QLabel(self)
#        self.title.setGeometry(200, 0, 990,62)
#        self.title.setPixmap(QtGui.QPixmap(os.getcwd() + "/Background.png"))

        self.pic = QtGui.QLabel(self)
        self.pic.setGeometry(200, 150, 300,243)
        self.pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/no-video.png"))
        
        self.no_pics = QtGui.QLabel('Number of Pictures Taken : ',self)
        self.no_pics.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.setStyleSheet("QLabel { font-size: 20pt; color:%s }" %  QtGui.QColor(255, 255, 255).name())
        self.no_pics.move(50,600)
        
     #   self.no_pics_taken = 0
     #   self.no_vids_taken = 0
        
        self.no_pics_lcd = QtGui.QLCDNumber(self)
        self.no_pics_lcd.move(400,607)
        self.no_pics_lcd.setNumDigits(2)
        self.no_pics_lcd.setFrameStyle(QtGui.QFrame.NoFrame);
     #   self.no_pics_lcd.display(self.no_pics_taken)
        
        self.no_vids = QtGui.QLabel('  Number of Videos Taken : ',self)
        self.no_vids.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.setStyleSheet("QLabel { font-size: 20pt; color:%s }" %  QtGui.QColor(255, 255, 255).name())
        self.no_vids.move(50,670)

        self.no_vids_lcd = QtGui.QLCDNumber(self)
        self.no_vids_lcd.move(400,677)
        self.no_vids_lcd.setNumDigits(2)
        self.no_vids_lcd.setFrameStyle(QtGui.QFrame.NoFrame);
     #   self.no_vids_lcd.display(self.no_vids_taken)
        
        self.distance_label = QtGui.QLabel('Distance Travelled : ',self)
        self.distance_label.setFont(QtGui.QFont("Times", 30, QtGui.QFont.Bold))
        self.setStyleSheet("QLabel { font-size: 20pt; color:%s }" %  QtGui.QColor(255, 255, 255).name())
        self.distance_label.move(750,80)
        
        self.distance_lcd = QtGui.QLCDNumber(self)
        self.distance_lcd.move(780,100)
        self.distance_lcd.setNumDigits(6)
        self.distance_lcd.resize(150,150)
        self.distance_lcd.setFrameStyle(QtGui.QFrame.NoFrame);
        self.distance_lcd.display(self.distance_travelled)

        self.speedometer = QtGui.QLabel(self)
        self.speedometer.setGeometry(670, 160, 300,300)
        self.speedometer.setPixmap(QtGui.QPixmap(os.getcwd() + "/speedometer3.png"))
        
#        self.needle = QtGui.QLabel(self)
#        self.needle.setGeometry(702, 130, 300,300)
#        self.needle_pix = QtGui.QPixmap(os.getcwd() + "/needle3.png")
#        self.needle_pix = self.needle_pix.transformed(QtGui.QTransform().translate(400,400))
#        self.needle_pix = self.needle_pix.transformed(QtGui.QTransform().rotate(90,40,40))
#        self.needle.setPixmap(self.needle_pix)

#        self.qp = QtGui.QPainter()
#        self.qp.begin(self)

#        self.pen = QtGui.QPen(QtCore.Qt.red, 10, QtCore.Qt.SolidLine)
#        self.qp.setPen(self.pen)
#        self.qp.drawLine(20, 40, 500, 40) 
#        self.qp.end()
        
        
        self.flag0_pix = QtGui.QPixmap(os.getcwd() + "/flag00.png")
        self.flag1_pix = QtGui.QPixmap(os.getcwd() + "/flag01.png")
        self.no_flags = 0
        
        self.flag = []
        self.flag.append(QtGui.QLabel(self))
        self.flag.append(QtGui.QLabel(self))
        self.flag.append(QtGui.QLabel(self))
        self.flag.append(QtGui.QLabel(self))
        self.flag.append(QtGui.QLabel(self))
        self.flag[0].setGeometry(1120, 50, 40,38)
        self.flag[1].setGeometry(1170, 50, 40,38)
        self.flag[2].setGeometry(1220, 50, 40,38)
        self.flag[3].setGeometry(1270, 50, 40,38)
        self.flag[4].setGeometry(1320, 50, 40,38)
        
        for i in range(5):
            self.flag[i].setPixmap(self.flag0_pix)

        self.claw0_pix = QtGui.QPixmap(os.getcwd() + "/claw0.png")
        self.claw1_pix = QtGui.QPixmap(os.getcwd() + "/claw1.png")
        self.no_claws = 0
        
        self.claw = []
        self.claw.append(QtGui.QLabel(self))
        self.claw.append(QtGui.QLabel(self))
        self.claw.append(QtGui.QLabel(self))
        self.claw.append(QtGui.QLabel(self))
        self.claw.append(QtGui.QLabel(self))
        self.claw[0].setGeometry(1120, 100, 40,38)
        self.claw[1].setGeometry(1170, 100, 40,38)
        self.claw[2].setGeometry(1220, 100, 40,38)
        self.claw[3].setGeometry(1270, 100, 40,38)
        self.claw[4].setGeometry(1320, 100, 40,38)
        
        for i in range(5):
            self.claw[i].setPixmap(self.claw0_pix)
        


        self.btn_slt0 = QtGui.QLabel(self)
        self.btn_slt0.setGeometry(900, 250, 30,30)
        self.btn_slt0_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/softleft0.png")
        self.btn_slt0.setPixmap(self.btn_slt0_pix)

        self.btn_str0 = QtGui.QLabel(self)
        self.btn_str0.setGeometry(965, 250, 30,30)
        self.btn_str0_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/up0.png")
        self.btn_str0.setPixmap(self.btn_str0_pix)

        self.btn_srt0 = QtGui.QLabel(self)
        self.btn_srt0.setGeometry(1030, 250, 30,30)
        self.btn_srt0_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/softright0.png")
        self.btn_srt0.setPixmap(self.btn_srt0_pix)

        self.btn_lft0 = QtGui.QLabel(self)
        self.btn_lft0.setGeometry(900, 305, 30,30)
        self.btn_lft0_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/left0.png")
        self.btn_lft0.setPixmap(self.btn_lft0_pix)

#        self.btn_stp0 = QtGui.QLabel(self)
#        self.btn_stp0.setGeometry(965, 305, 30,30)
#        self.btn_slt0_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/softleft0.png")
#        self.btn_slt0.setPixmap(self.btn_slt0_pix)

        self.btn_rgt0 = QtGui.QLabel(self)
        self.btn_rgt0.setGeometry(1030, 305, 30,30)
        self.btn_rgt0_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/right0.png")
        self.btn_rgt0.setPixmap(self.btn_rgt0_pix)

        self.btn_rlt0 = QtGui.QLabel(self)
        self.btn_rlt0.setGeometry(900, 360, 30,30)
        self.btn_rlt0_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/softRright0.png")
        self.btn_rlt0.setPixmap(self.btn_rlt0_pix)

        self.btn_rev0 = QtGui.QLabel(self)
        self.btn_rev0.setGeometry(965, 360, 30,30)
        self.btn_rev0_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/down0.png")
        self.btn_rev0.setPixmap(self.btn_rev0_pix)

        self.btn_rrt0 = QtGui.QLabel(self)
        self.btn_rrt0.setGeometry(1030, 360, 30,30)
        self.btn_rrt0_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/softRleft0.png")
        self.btn_rrt0.setPixmap(self.btn_rrt0_pix)

        self.btn_slt1 = QtGui.QLabel(self)
        self.btn_slt1.setGeometry(900, 250, 30,30)
        self.btn_slt1_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/softleft1.png")

        self.btn_str1 = QtGui.QLabel(self)
        self.btn_str1.setGeometry(965, 250, 30,30)
        self.btn_str1_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/up1.png")

        self.btn_srt1 = QtGui.QLabel(self)
        self.btn_srt1.setGeometry(1030, 250, 30,30)
        self.btn_srt1_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/softright1.png")

        self.btn_lft1 = QtGui.QLabel(self)
        self.btn_lft1.setGeometry(900, 305, 30,30)
        self.btn_lft1_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/left1.png")

#        self.btn_stp1 = QtGui.QLabel(self)
#        self.btn_stp1.setGeometry(965, 305, 30,30)
#        self.btn_stp1_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/softleft0.png")

        self.btn_rgt1 = QtGui.QLabel(self)
        self.btn_rgt1.setGeometry(1030, 305, 30,30)
        self.btn_rgt1_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/right1.png")

        self.btn_rlt1 = QtGui.QLabel(self)
        self.btn_rlt1.setGeometry(900, 360, 30,30)
        self.btn_rlt1_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/softRright1.png")

        self.btn_rev1 = QtGui.QLabel(self)
        self.btn_rev1.setGeometry(965, 360, 30,30)
        self.btn_rev1_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/down1.png")

        self.btn_rrt1 = QtGui.QLabel(self)
        self.btn_rrt1.setGeometry(1030, 360, 30,30)
        self.btn_rrt1_pix = QtGui.QPixmap(os.getcwd() + "/Arrows/softRleft1.png")

        self.video_feed = QtGui.QPushButton("Begin Video Feed",self)
        self.video_feed.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.video_feed.move(1150,250)
        self.video_feed.clicked.connect(self.videoFeedButtonClicked)

        self.take_picture = QtGui.QPushButton("Take Picture",self)
        self.take_picture.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.take_picture.move(1165,300)
        self.take_picture.clicked.connect(self.takePictureButtonClicked)
        self.take_picture.setShortcut('Z')

        self.take_video = QtGui.QPushButton("Take Video",self)
        self.take_video.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.take_video.move(1170,350)
        self.take_video.clicked.connect(self.takeVideoButtonClicked)
        self.take_video.setShortcut('X')
        
        
        '''
        # Draw MenuBar
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+W')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
        self.statusBar().showMessage('Ready')
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        # End MenuBar
        '''
        self.show()
        subprocess.Popen(["wmctrl -a 'Control Center | Team X-Men, IIT Madras'"],shell=True)
        
        self.timer = QtCore.QTimer(self)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update_distance)
        self.timer.start(1000)
    
    def update_distance(self):
        response = self.BBB.sendMsg(('enc',''))
        self.updateDistance(response)
        self.distance_lcd.display(self.distance_travelled)
        
        
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            subprocess.Popen(["wmctrl -c 'Team X-men - Live Feed'"],shell=True)
            self.f.close()
            self.BBB.sendCmd(('asdfb',''))
            self.close()
        elif e.key() == QtCore.Qt.Key_7:
            self.btn_slt1.setPixmap(self.btn_slt1_pix)
            response = self.BBB.sendCmd(('drv','slt'))
        elif e.key() == QtCore.Qt.Key_8:
            self.btn_str1.setPixmap(self.btn_str1_pix)
            response = self.BBB.sendCmd(('drv','str'))
        elif e.key() == QtCore.Qt.Key_9:
            self.btn_srt1.setPixmap(self.btn_srt1_pix)
            response = self.BBB.sendCmd(('drv','srt'))
        elif e.key() == QtCore.Qt.Key_4:
            self.btn_lft1.setPixmap(self.btn_lft1_pix)
            response = self.BBB.sendCmd(('drv','lft'))
        elif e.key() == QtCore.Qt.Key_5:
            response = self.BBB.sendCmd(('drv','stp'))
        elif e.key() == QtCore.Qt.Key_6:
            self.btn_rgt1.setPixmap(self.btn_rgt1_pix)
            response = self.BBB.sendCmd(('drv','rgt'))
        elif e.key() == QtCore.Qt.Key_1:
            self.btn_rlt1.setPixmap(self.btn_rlt1_pix)
            response = self.BBB.sendCmd(('drv','rlt'))
        elif e.key() == QtCore.Qt.Key_2:
            self.btn_rev1.setPixmap(self.btn_rev1_pix)
            response = self.BBB.sendCmd(('drv','rev'))
        elif e.key() == QtCore.Qt.Key_3:
            self.btn_rrt1.setPixmap(self.btn_rrt1_pix)
            response = self.BBB.sendCmd(('drv','rrt'))
            
        elif e.key() == QtCore.Qt.Key_P:
            if self.no_flags<5:
                self.no_flags = self.no_flags+1
            for i in range(self.no_flags):
                self.flag[i].setPixmap(self.flag1_pix)
            
        elif e.key() == QtCore.Qt.Key_O:
            if self.no_flags>0:
                self.no_flags = self.no_flags-1
            for i in range(self.no_flags,5):
                self.flag[i].setPixmap(self.flag0_pix)

        elif e.key() == QtCore.Qt.Key_L:
            if self.no_claws<5:
                self.no_claws = self.no_claws+1
            for i in range(self.no_claws):
                self.claw[i].setPixmap(self.claw1_pix)
            
        elif e.key() == QtCore.Qt.Key_K:
            if self.no_claws>0:
                self.no_claws = self.no_claws-1
            for i in range(self.no_claws,5):
                self.claw[i].setPixmap(self.claw0_pix)


    def keyReleaseEvent(self, e):
            if e.key() == QtCore.Qt.Key_7:
                self.btn_slt1.clear()
                response = self.BBB.sendCmd(('drv','stp'))
            elif e.key() == QtCore.Qt.Key_8:
                self.btn_str1.clear()
                response = self.BBB.sendCmd(('drv','stp'))
            elif e.key() == QtCore.Qt.Key_9:
                self.btn_srt1.clear()
                response = self.BBB.sendCmd(('drv','stp'))
            elif e.key() == QtCore.Qt.Key_4:
                self.btn_lft1.clear()
                response = self.BBB.sendCmd(('drv','stp'))
#            if e.key() == QtCore.Qt.Key_5:
#                self.btn_slt1.clear()
            elif e.key() == QtCore.Qt.Key_6:
                self.btn_rgt1.clear()
                response = self.BBB.sendCmd(('drv','stp'))
            elif e.key() == QtCore.Qt.Key_1:
                self.btn_rlt1.clear()
                response = self.BBB.sendCmd(('drv','stp'))
            elif e.key() == QtCore.Qt.Key_2:
                self.btn_rev1.clear()
                response = self.BBB.sendCmd(('drv','stp'))
            elif e.key() == QtCore.Qt.Key_3:
                self.btn_rrt1.clear()
                response = self.BBB.sendCmd(('drv','stp'))
            
                
    
    def videoFeedButtonClicked(self):
        response = self.BBB.sendMsg(('vds',''))
#        QtGui.QMessageBox.question(self, 'Message', response, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        if response:
            self.videofeed_pid = subprocess.Popen(VIDEOFEED_LAUNCH,shell=True).pid
            break_loop = 0
            while 1:
                lines = commands.getoutput("wmctrl -l").split("\n")
                for line in lines:
                    line = line.replace("  ", " ")
                    win = tuple(line.split(" ", 3))
                    if 'gst-launch-0.10' in win[3]:
                        break_loop = 1;
                if break_loop == 1:
                    break
                else:
                    print "gst-launch not yet opened"
    
            subprocess.Popen(["wmctrl -r gst-launch-0.10 -T \"Team X-men - Live Feed\""],shell=True)
            subprocess.Popen(["wmctrl -r 'Team X-men - Live Feed' -e 0,15,84,640,480"],shell=True)
            subprocess.Popen(["wmctrl -r 'Team X-men - Live Feed' -b toggle,above"],shell=True)
            
            w = gtk.gdk.window_foreign_new( gtk.gdk.get_default_root_window().property_get("_NET_ACTIVE_WINDOW")[2][0] )
            w.set_decorations( (w.get_decorations()+1)%2 ) # toggle between 0 and 1
            gtk.gdk.window_process_all_updates()
            gtk.gdk.flush()
            subprocess.Popen(["wmctrl -a 'Control Center | Team X-Men, IIT Madras'"],shell=True)
    
    def takePictureButtonClicked(self):
        response = self.BBB.sendMsg(('img',''))
    #    self.no_pics_taken=self.no_pics_taken+1
    #    self.no_pics_lcd.display(self.no_pics_taken)
        self.f.write("Image TimeStamp:" + strftime("%Y-%m-%d %H:%M:%S") + " Distance:" + str(self.distance_travelled) +" Team_ID:1 Cam_ID:2 \n")

    def takeVideoButtonClicked(self):
        response = self.BBB.sendMsg(('vid',''))
    #    self.no_vids_taken=self.no_vids_taken+1
    #    self.no_vids_lcd.display(self.no_vids_taken)
        self.f.write("Video TimeStamp:" + strftime("%Y-%m-%d %H:%M:%S") + " Distance:" + str(self.distance_travelled) +" Team_ID:1 Cam_ID:2 \n")
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    t = Console()
    sys.exit(app.exec_())
    
