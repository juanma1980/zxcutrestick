#!/usr/bin/python3
from PySide2.QtWidgets import QApplication ,QMainWindow,QPushButton,QVBoxLayout,QWidget,QLabel
from PySide2 import QtGui
from PySide2.QtCore import QSize,Slot,Qt, QPropertyAnimation,QThread,QRect,QTimer,Signal,QSignalMapper,QProcess,QEvent
import time
import subprocess

class virtupal(QWidget):
	def __init__(self,*args):
		super().__init__()
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		#self.setWindowModality(Qt.WindowModal)
		self.setAttribute(Qt.WA_ShowWithoutActivating)
		self.setFocusPolicy(Qt.NoFocus)
		self.pos=20
		self.radius=200
		self.setGeometry(self.pos, self.pos, self.radius+30, self.radius+30)
		self.stick=QPushButton("*")
		self.size=40
		self.setMouseTracking(True) 
		self.drawStick()
		self.show()

	def paintEvent(self,*args):
		painter=QtGui.QPainter(self)
		painter.setPen(QtGui.QPen(Qt.green,8,Qt.DashLine))
		painter.drawRect(self.pos,self.pos,self.radius,self.radius)

	def drawStick(self):
		lay=QVBoxLayout()
		self.stick.setAutoRepeat(True)
		self.stick.setFixedSize(self.size*2,self.size*2)
		self.stick.setStyleSheet("border: 1px solid blue;border-radius: {}px;".format(self.size))
		#self.stick.pressed.connect(self._move)
		self.stick.setFocusPolicy(Qt.NoFocus)
		lay.addWidget(self.stick)
		self.setLayout(lay)

	def mouseMoveEvent(self, qtevent):
		posx=qtevent.x()
		posy=qtevent.y()
		keyx=""
		keyy=""
		tolerance=20
		if posx>(self.radius/2)-tolerance and posx<(self.radius/2)+tolerance:
			posx=self.radius/2
			keyx=""
		elif posx<self.radius/2:
			keyx="o"
			posx=0
		elif posx>self.radius/2:
			keyx="p"
			posx=self.radius
		if posy>(self.radius/2)-tolerance and posy<(self.radius/2)+tolerance:
			keyy=""
			posy=self.radius/2
		elif posy<self.radius/2:
			keyy="q"
			posy=0
		elif posx>self.radius/2:
			keyy="a"
			posy=self.radius
		self.stick.move(posx,posy)
		if keyx or keyy:
			if keyx and keyy:
				cmd=["xdotool","key","{}+{}".format(keyx,keyy)]
			elif keyx:
				cmd=["xdotool","key",keyx]
			elif keyy:
				cmd=["xdotool","key",keyy]
			subprocess.run(cmd)
		time.sleep(0.01)

 

app=QApplication(["Virtupal"])
virtupalLauncher=virtupal()
app.exec_()

