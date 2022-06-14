#!/usr/bin/python3
#Copyright juanma1980 2022
#Gpl-3 License
from PySide2.QtWidgets import QApplication ,QMainWindow,QPushButton,QVBoxLayout,QWidget,QHBoxLayout
from PySide2 import QtGui
from PySide2.QtCore import Qt,QThread,QRect,QEvent,QThread
import os,time
import subprocess

class pressedBtnFire(QThread):
	def __init__(self,*args):
		super().__init__()
		self.fire1="space"
		self.fire2=""
	#def __init__

	def setKeys(self,fire1="espace",fire2=""):
		self.fire1=fire1
		self.fire2=fire2
	#def setKeys

	def run(self,*args):
		cmd=["xdotool","keydown",self.fire1]
		subprocess.run(cmd)
		time.sleep(0.01)
		cmd=["xdotool","keyup",self.fire1]
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
		self.config={'fire1':'space','fire2':''}
		self.size=128
		self.btnFire1=QPushButton(self.config['fire1'])
		self.btnFire1.setAttribute(Qt.WA_AcceptTouchEvents)
		self.setAttribute(Qt.WA_AcceptTouchEvents)
		self.drawButtons()
		self.show()
		self._setPosition()
	#def __init__

	def setKeys(self,config):
		for key,item in config.items():
			if key in self.config.keys():
				self.config[key]=item
		self.btnFire1.setText(self.config['fire1'])
		self.pressedBtnFire.setKeys(self.config['fire1'],self.config['fire2'])
	#def setKeys

	def _setPosition(self):
		scr=app.primaryScreen()
		w=scr.size().width()
		h=scr.size().height()
		self.move(0+(self.size*0.5),h-(self.size*1.5))
	#def _setPosition

	def eventFilter(self,source,event):
		if event.type()==QEvent.Type.TouchBegin:
			self.pressedBtnFire.start()
		return True
	#def eventFilter

	def drawButtons(self):
		lay=QHBoxLayout()
		self.btnFire1.setAutoRepeat(True)
		self.btnFire1.setFixedSize(self.size,self.size)
		self.btnFire1.setStyleSheet("border: 1px solid blue;border-radius: {}px;".format(self.size))
		self.btnFire1.setFocusPolicy(Qt.NoFocus)
		lay.addWidget(self.btnFire1)
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
		self.setFocusPolicy(Qt.NoFocus)
		self.installEventFilter(self)
		self.pressedStick=pressedStick()
		self.config={'left':'o','right':'p','up':'q','down':'a'}
		self.border=20
		self.pos=self.border/2
		self.radius=150
		self.setGeometry(self.pos, self.pos, self.radius+self.border, self.radius+self.border)
		self.swMoving=False
		self.swTouch=False
		self.stick=QPushButton("*")
		self.stick.setAttribute(Qt.WA_AcceptTouchEvents)
		self.size=100
		self.grabMouse()
		self.setMouseTracking(True) 
		self.drawStick()
		self.show()
		self._setPosition()
	#def __init__

	def setKeys(self,config):
		for key,item in config.items():
			if key in self.config.keys():
				self.config[key]=item
	#def setKeys

	def _setPosition(self):
		scr=app.primaryScreen()
		w=scr.size().width()
		h=scr.size().height()
		self.move(w-(self.radius+(self.size)),h-(self.radius+(self.size)))
	#def _setPosition

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
	#def eventFilter
	
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
			keyx=self.config['left']
			posx=self.border
		elif posx>self.radius/2:
			keyx=self.config['right']
			posx=centerX+self.border
		if posy>centerY-toleranceL and posy<centerY+toleranceR:
			keyy=""
			posy=centerY
		elif posy<self.radius/2:
			keyy=self.config['up']
			posy=self.border
		elif posy>self.radius/2:
			keyy=self.config['down']
			posy=centerY+self.border
		self.stick.move(posx,posy)
		self.pressedStick.setKeys(x=keyx,y=keyy)
		self.pressedStick.start()
	#def moveStick
#class cutrestick

def _parseConfig():
	config="./config.txt"
	contents=[]
	if os.path.isfile(config):
		with open(config,"r") as f:
			contents=f.readlines()
	config={'left':'o','right':'p','up':'q','down':'a','fire1':'space','fire2':''}
	for line in contents:
		if line.startswith("left"):
			config['left']=line.split("=")[-1].strip()
		elif line.startswith("right"):
			config['right']=line.split("=")[-1].strip()
		elif line.startswith("down"):
			config['down']=line.split("=")[-1].strip()
		elif line.startswith("up"):
			config['up']=line.split("=")[-1].strip()
		elif line.startswith("fire1"):
			config['fire1']=line.split("=")[-1].strip()
		elif line.startswith("fire2"):
			config['fire2']=line.split("=")[-1].strip()
	return config
#def parseConfig
	

app=QApplication(["cutreStick"])
cutreStick=cutrestick()
cutreButtons=cutrebuttons()
config=_parseConfig()
cutreStick.setKeys(config)
cutreButtons.setKeys(config)
app.exec_()

