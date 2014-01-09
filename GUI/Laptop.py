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
import PyQt4.Qwt5 as Qwt


from PyQt4 import QtGui, QtCore
from x_men_lp_defns import *               # Import definitions for Laptop

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

class Console(QtGui.QWidget):
    def __init__(self):
        super(Console, self).__init__()
        self.BBB = Comms()
        self.initUI()
        
    def initUI(self):

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

        subprocess.Popen(["gst-launch udpsrc port=5000 ! smokedec ! autovideosink"],shell=True)
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
        subprocess.Popen(["wmctrl -r 'Team X-men - Live Feed' -e 0,15,84,-1,-1"],shell=True)
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
        self.pic.setGeometry(15, 60, 640,480)
        self.pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/Screenshot.png"))
        
        self.no_pics = QtGui.QLabel('Number of Pictures Taken : ',self)
        self.no_pics.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.setStyleSheet("QLabel { font-size: 20pt; color:%s }" %  QtGui.QColor(255, 255, 255).name())
        self.no_pics.move(50,580)
        
        self.no_pics_lcd = QtGui.QLCDNumber(self)
        self.no_pics_lcd.move(400,587)
        self.no_pics_lcd.setNumDigits(2)
        self.no_pics_lcd.setFrameStyle(QtGui.QFrame.NoFrame);
        
#        self.palette = self.no_pics_lcd.palette()
#        # foreground color
#        self.palette.setColor(self.palette.WindowText, QtGui.QColor(85, 85, 255))
#        # background color
#        self.palette.setColor(self.palette.Background, QtGui.QColor(255, 170, 255))
#        # "light" border
#        self.palette.setColor(self.palette.Light, QtGui.QColor(255, 255, 255))
#        # "dark" border
#        self.palette.setColor(self.palette.Dark, QtGui.QColor(0, 255, 0))
#        # set the palette
#        self.no_pics_lcd.setPalette(self.palette)

        self.no_vids = QtGui.QLabel('  Number of Videos Taken : ',self)
        self.no_vids.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))
        self.setStyleSheet("QLabel { font-size: 20pt; color:%s }" %  QtGui.QColor(255, 255, 255).name())
        self.no_vids.move(50,650)

        self.no_vids_lcd = QtGui.QLCDNumber(self)
        self.no_vids_lcd.move(400,657)
        self.no_vids_lcd.setNumDigits(2)
        self.no_vids_lcd.setFrameStyle(QtGui.QFrame.NoFrame);

        self.btn_slt = QtGui.QPushButton(self)
        self.btn_slt.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.btn_slt.move(900,250)
        self.icon = QtGui.QIcon("google.png")
        self.btn_slt.setIcon(self.icon)
        self.btn_slt.setIconSize(QtCore.QSize(40,40))
        self.btn_slt.setShortcut('Q')
        
        self.btn_str = QtGui.QPushButton(self)
        self.btn_str.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.btn_str.move(965,250)
        self.icon = QtGui.QIcon("lena.jpg")
        self.btn_str.setIcon(self.icon)
        self.btn_str.setIconSize(QtCore.QSize(40,40))
        self.btn_str.setShortcut('UpArrow')

        self.btn_srt = QtGui.QPushButton(self)
        self.btn_srt.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.btn_srt.move(1030,250)
        self.icon = QtGui.QIcon("google.png")
        self.btn_srt.setIcon(self.icon)
        self.btn_srt.setIconSize(QtCore.QSize(40,40))

        self.btn_lft = QtGui.QPushButton(self)
        self.btn_lft.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.btn_lft.move(900,305)
        self.icon = QtGui.QIcon("google.png")
        self.btn_lft.setIcon(self.icon)
        self.btn_lft.setIconSize(QtCore.QSize(40,40))

        self.btn_stp = QtGui.QPushButton(self)
        self.btn_stp.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.btn_stp.move(965,305)
        self.icon = QtGui.QIcon("google.png")
        self.btn_stp.setIcon(self.icon)
        self.btn_stp.setIconSize(QtCore.QSize(40,40))

        self.btn_rgt = QtGui.QPushButton(self)
        self.btn_rgt.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.btn_rgt.move(1030,305)
        self.icon = QtGui.QIcon("google.png")
        self.btn_rgt.setIcon(self.icon)
        self.btn_rgt.setIconSize(QtCore.QSize(40,40))

        self.btn_rlt = QtGui.QPushButton(self)
        self.btn_rlt.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.btn_rlt.move(900,360)
        self.icon = QtGui.QIcon("google.png")
        self.btn_rlt.setIcon(self.icon)
        self.btn_rlt.setIconSize(QtCore.QSize(40,40))

        self.btn_rev = QtGui.QPushButton(self)
        self.btn_rev.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.btn_rev.move(965,360)
        self.icon = QtGui.QIcon("google.png")
        self.btn_rev.setIcon(self.icon)
        self.btn_rev.setIconSize(QtCore.QSize(40,40))

        self.btn_rrt = QtGui.QPushButton(self)
        self.btn_rrt.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.btn_rrt.move(1030,360)
        self.icon = QtGui.QIcon("google.png")
        self.btn_rrt.setIcon(self.icon)
        self.btn_rrt.setIconSize(QtCore.QSize(40,40))

        
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
        
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            subprocess.Popen(["wmctrl -c 'Team X-men - Live Feed'"],shell=True)
            self.close()
        
    
    def buttonClicked(self):
        response = self.BBB.sendMsg(('vds',''))
        QtGui.QMessageBox.question(self, 'Message', response, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        if response:
            self.videofeed_pid = subprocess.Popen(VIDEOFEED_LAUNCH,shell=True).pid
            
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    t = Console()
    sys.exit(app.exec_())
