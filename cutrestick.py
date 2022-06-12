#!/usr/bin/python3
from PySide2.QtWidgets import QApplication ,QMainWindow,QPushButton,QVBoxLayout,QWidget,QLabel,QHBoxLayout
from PySide2 import QtGui
from PySide2.QtCore import QSize,Slot,Qt, QPropertyAnimation,QThread,QRect,QTimer,Signal,QSignalMapper,QProcess,QEvent,QThread
import time
import subprocess

class pressedStick(QThread):
	def __init__(self,*args):
		super().__init__()
		self.keyx=""
		self.keyy=""
	#def __init__

	def run(self,*args):
		while True:
			if self.keyx or self.keyy:
				if self.keyx and self.keyy:
					cmd=["xdotool","key","{}+{}".format(self.keyx,self.keyy)]
				elif self.keyx:
					cmd=["xdotool","key",self.keyx]
				elif self.keyy:
					cmd=["xdotool","key",self.keyy]
				subprocess.run(cmd)
			QApplication.processEvents()
			time.sleep(0.01)
	#def run

	def setKeys(self,x="",y=""):
		self.keyx=x
		self.keyy=y
	#def setKeys
#class pressedStick

class cutrebuttons(QWidget):
	def __init__(self,*args):
		super().__init__()
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		#self.setWindowModality(Qt.WindowModal)
		self.setAttribute(Qt.WA_ShowWithoutActivating)
		self.setFocusPolicy(Qt.NoFocus)
		self.pressedStick=pressedStick()
		self.pos=20
		self.radius=100
		self.setGeometry(self.pos, self.pos, self.radius+30, self.radius+30)
		self.btnM=QPushButton("M")
		self.size=128
		self.drawButtons()
		self.show()
		self.move(600,600)
		#self.pressedStick.start()
	#def __init__

	def drawButtons(self):
		lay=QHBoxLayout()
		self.btnM.setAutoRepeat(True)
		self.btnM.setFixedSize(self.size,self.size)
		self.btnM.setStyleSheet("border: 1px solid blue;border-radius: {}px;".format(self.size))
		#self.stick.pressed.connect(self._move)
		self.btnM.setFocusPolicy(Qt.NoFocus)
		self.btnM.clicked.connect(self._sendM)
		lay.addWidget(self.btnM)
		self.setLayout(lay)
	#def drawButtons

	def _sendM(self):
		cmd=["xdotool","key","m"]
		subprocess.run(cmd)
	#def _sendM(self):
#class cutrebuttons

class cutrestick(QWidget):
	def __init__(self,*args):
		super().__init__()
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		#self.setWindowModality(Qt.WindowModal)
		self.setAttribute(Qt.WA_ShowWithoutActivating)
		self.setFocusPolicy(Qt.NoFocus)
		self.pressedStick=pressedStick()
		self.pos=20
		self.radius=200
		self.setGeometry(self.pos, self.pos, self.radius+30, self.radius+30)
		self.stick=QPushButton("*")
		self.size=40
		self.setMouseTracking(True) 
		self.drawStick()
		self.show()
		self.move(200,200)
		self.pressedStick.start()
	#def __init__

	def paintEvent(self,*args):
		painter=QtGui.QPainter(self)
		painter.setPen(QtGui.QPen(Qt.green,8,Qt.DashLine))
		painter.drawRect(self.pos,self.pos,self.radius,self.radius)
	#def paintEvent

	def drawStick(self):
		lay=QVBoxLayout()
		self.stick.setAutoRepeat(True)
		self.stick.setFixedSize(self.size*2,self.size*2)
		self.stick.setStyleSheet("border: 1px solid blue;border-radius: {}px;".format(self.size))
		#self.stick.pressed.connect(self._move)
		self.stick.setFocusPolicy(Qt.NoFocus)
		lay.addWidget(self.stick)
		self.setLayout(lay)
	#def drawStick

	def mouseReleaseEvent(self, qtevent):
		self.pressedStick.setKeys(x="",y="")
		self.stick.move(self.radius/2,self.radius/2)
	#def mouseReleaseEvent

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
		elif posy>self.radius/2:
			keyy="a"
			posy=self.radius
		self.stick.move(posx,posy)
		self.pressedStick.setKeys(x=keyx,y=keyy)
	#def mouseMoveEvent
#class cutrestick

app=QApplication(["cutreStick"])
cutreStick=cutrestick()
cutreButtons=cutrebuttons()
app.exec_()

