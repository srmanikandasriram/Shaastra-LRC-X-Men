#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Team X-Men IIT Madras.
Control Console for Shaastr Lunar Rover Challenge 2014
"""

import sys
from PyQt4 import QtGui, QtCore

class Template(QtGui.QWidget):
    def __init__(self):
        super(Template, self).__init__()
        self.initUI()
        
    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.setToolTip('This is the control panel of <b>Team X-Men</b> for <b>LRC 2014</b>.')

        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)
        
        self.title = QtGui.QLabel('Control Console of Team X-Men, IIT Madras for LRC 2014')
        self.grid.addWidget(self.title,0,0)
        
        self.lcd = QtGui.QLCDNumber(self)
        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.sld.valueChanged.connect(self.lcd.display)

        self.grid.addWidget(self.lcd,4,0,1,3)
        self.grid.addWidget(self.sld,5,0,1,3)
        keys = ['|-', '^', '-|', '<', '*', '>', 'L', 'v', '_|']
        j = 0
        key_pos = [(1, 0), (1, 1), (1, 2),
               (2, 0), (2, 1), (2, 2),
               (3, 0), (3, 1), (3, 2)]

        for i in keys:
            button = QtGui.QPushButton(i)
            self.grid.addWidget(button, key_pos[j][0], key_pos[j][1])
            j = j + 1

        self.setLayout(self.grid)   
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
        self.setGeometry(10, 10, 1366, 768)
        self.setWindowTitle('Control Center | Team X-Men, IIT Madras')
        self.setWindowIcon(QtGui.QIcon('google.png'))
        self.show()
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        self.lcd.display(e.key())

def main():
    app = QtGui.QApplication(sys.argv)
    t = Template()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
