#!/usr/bin/python3
from PySide2.QtWidgets import QApplication ,QMainWindow,QPushButton,QVBoxLayout,QWidget,QHBoxLayout
from PySide2 import QtGui
from PySide2.QtCore import Qt,QThread,QRect,QEvent,QThread
import time
import subprocess

class pressedBtnFire(QThread):
	def __init__(self,*args):
		super().__init__()
		self.key="m"
	#def __init__

	def run(self,*args):
		cmd=["xdotool","keydown","space"]
		subprocess.run(cmd)
		time.sleep(0.01)
		cmd=["xdotool","keyup","space"]
		subprocess.run(cmd)
		time.sleep(0.01)
		return True
	#def run
#class pressedBtnFire

class pressedStick(QThread):
	def __init__(self,*args):
		super().__init__()
		self.keyx=""
		self.keyy=""
		self.dbg=False
	#def __init__

	def _debug(self,msg):
		if self.dbg==True:
			print("stick: {}".format(msg))

	def run(self,*args):
		if self.keyx or self.keyy:
			if self.keyx and self.keyy:
				cmd=["xdotool","keydown","{}+{}".format(self.keyx,self.keyy)]
			elif self.keyx:
				cmd=["xdotool","keydown",self.keyx]
			elif self.keyy:
				cmd=["xdotool","keydown",self.keyy]
			subprocess.run(cmd)
			#QApplication.processEvents()
		return True
	#def run

	def setKeys(self,x="",y=""):
		if x!=self.keyx or y!=self.keyy:
			if y!=self.keyy or y=="":
				cmd=["xdotool","keyup",self.keyy]
				subprocess.run(cmd)
			if x!=self.keyx or x=="":
				cmd=["xdotool","keyup",self.keyx]
			subprocess.run(cmd)
			time.sleep(0.01)
		self.keyx=x
		self.keyy=y
		self._debug("Set keys {} {}".format(self.keyx,self.keyy))
	#def setKeys
#class pressedStick

class cutrebuttons(QWidget):
	def __init__(self,*args):
		super().__init__()
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		self.setAttribute(Qt.WA_ShowWithoutActivating)
		self.setFocusPolicy(Qt.NoFocus)
		self.pressedBtnFire=pressedBtnFire()
		self.installEventFilter(self)
		self.size=128
		self.btnFire=QPushButton("M")
		self.btnFire.setAttribute(Qt.WA_AcceptTouchEvents)
		self.setAttribute(Qt.WA_AcceptTouchEvents)
		self.drawButtons()
		self.show()
		self._setPosition()
	#def __init__

	def _setPosition(self):
		scr=app.primaryScreen()
		w=scr.size().width()
		h=scr.size().height()
		self.move(0+(self.size*0.5),h-(self.size*1.5))
	#def _setPosition(self):

	def eventFilter(self,source,event):
		if event.type()==QEvent.Type.TouchBegin:
			self.pressedBtnFire.start()
		return True
	#def eventFilter

	def drawButtons(self):
		lay=QHBoxLayout()
		self.btnFire.setAutoRepeat(True)
		self.btnFire.setFixedSize(self.size,self.size)
		self.btnFire.setStyleSheet("border: 1px solid blue;border-radius: {}px;".format(self.size))
		self.btnFire.setFocusPolicy(Qt.NoFocus)
		lay.addWidget(self.btnFire)
		self.setLayout(lay)
	#def drawButtons
#class cutrebuttons

class cutrestick(QWidget):
	def __init__(self,*args):
		super().__init__()
		self.setAttribute(Qt.WA_AcceptTouchEvents)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		self.setAttribute(Qt.WA_ShowWithoutActivating)
		self.setCursor(Qt.BlankCursor)
		self.installEventFilter(self)
		self.setFocusPolicy(Qt.NoFocus)
		self.grabMouse()
		self.pressedStick=pressedStick()
		self.border=20
		self.pos=self.border/2
		self.radius=150
		self.setGeometry(self.pos, self.pos, self.radius+self.border, self.radius+self.border)
		self.stick=QPushButton("*")
		self.size=100
		self.stick.setAttribute(Qt.WA_AcceptTouchEvents)
		self.setMouseTracking(True) 
		self.drawStick()
		self.show()
		self.swMoving=False
		self.swTouch=False
		self._setPosition()
	#def __init__

	def _setPosition(self):
		scr=app.primaryScreen()
		w=scr.size().width()
		h=scr.size().height()
		self.move(w-(self.radius+(self.size)),h-(self.radius+(self.size)))
	#def _setPosition(self):

	def paintEvent(self,*args):
		painter=QtGui.QPainter(self)
		painter.setPen(QtGui.QPen(Qt.green,8,Qt.DashLine))
		painter.drawRect(self.pos,self.pos,self.radius,self.radius)
	#def paintEvent

	def drawStick(self):
		lay=QVBoxLayout()
		self.stick.setAutoRepeat(True)
		self.stick.setFixedSize(self.size,self.size)
		self.stick.setStyleSheet("border: 1px solid blue;border-radius: {}px;".format(self.size*2))
		self.stick.setFocusPolicy(Qt.NoFocus)
		lay.addWidget(self.stick)
		self.stick.move((self.radius/2)-self.size,(self.radius/2)-self.size)
		self.setLayout(lay)
	#def drawStick

	def eventFilter(self,source,event):
		if event.type()==QEvent.Type.TouchBegin:
			self.swTouch=True
		elif event.type()==QEvent.Type.MouseMove and self.swTouch:
			self._moveStick(event.x(),event.y())
		elif event.type()==QEvent.Type.MouseButtonRelease or event.type()==QEvent.Type.TouchEnd:
			self.swTouch=False
			self.stick.move((self.width()/2)-self.size/2,(self.height()/2)-self.size/2)
			self.pressedStick.setKeys(x="",y="")
		return False
	
	def _moveStick(self, posx,posy):
		keyx=""
		keyy=""
		centerX=((self.width()/2)-self.size/2)
		centerY=((self.height()/2)-self.size/2)
		toleranceR=self.size/2.5
		toleranceL=self.size/2.5
		if posx>centerX-toleranceL and posx<centerX+toleranceR:
			posx=centerX
			keyx=""
		elif posx<self.radius/2:
			keyx="o"
			posx=self.border
		elif posx>self.radius/2:
			keyx="p"
			posx=centerX+self.border
		if posy>centerY-toleranceL and posy<centerY+toleranceR:
			keyy=""
			posy=centerY
		elif posy<self.radius/2:
			keyy="q"
			posy=self.border
		elif posy>self.radius/2:
			keyy="a"
			posy=centerY+self.border
		self.stick.move(posx,posy)
		self.pressedStick.setKeys(x=keyx,y=keyy)
		self.pressedStick.start()
	#def mouseMoveEvent
#class cutrestick

app=QApplication(["cutreStick"])
cutreStick=cutrestick()
cutreButtons=cutrebuttons()
app.exec_()

