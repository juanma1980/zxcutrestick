#!/usr/bin/python3
#Copyright juanma1980 2022
#Gpl-3 License
from PySide2.QtWidgets import QApplication ,QMainWindow,QPushButton,QVBoxLayout,QWidget,QGridLayout
from PySide2 import QtGui
from PySide2.QtCore import Qt,QThread,QRect,QEvent,QThread,QSize
import os,time
import subprocess

class pressedBtn(QThread):
	def __init__(self,*args):
		super().__init__()
		self.key="space"
		self.latency=0.1
	#def __init__

	def setKey(self,key="space"):
		self.key=key
	#def setKey

	def run(self,*args):
		if self.key=="X":
			self._cutreQuit()
		else:
			cmd=["xdotool","keydown",self.key]
			subprocess.run(cmd)
			time.sleep(self.latency)
			cmd=["xdotool","keyup",self.key]
			subprocess.run(cmd)
			time.sleep(self.latency)
		return True
	#def run

	def setLatency(self,latency):
		self.latency=latency
	#def setLatency

	def _cutreQuit(self,*args):
		QApplication.quit()
	#def _cutreQuit(self,*args):
#class pressedBtnFire

class pressedStick(QThread):
	def __init__(self,*args):
		super().__init__()
		self.keyx=""
		self.oldkeyx=""
		self.keyy=""
		self.oldkeyy=""
		self.latency=0.1
	#def __init__

	def run(self,*args):
		if self.keyx or self.keyy:
			if self.keyx and self.keyy:
				cmd=["xdotool","keydown","{}+{}".format(self.keyx,self.keyy)]
			elif self.keyx:
				cmd=["xdotool","keydown",self.keyx]
			elif self.keyy:
				cmd=["xdotool","keydown",self.keyy]
			subprocess.run(cmd)
			time.sleep(self.latency)
		return True
	#def run

	def setKeys(self,x="",y=""):
		if self.oldkeyy!="" and self.oldkeyy!=self.keyy:
			cmd=["xdotool","keyup",self.oldkeyy]
			subprocess.run(cmd)
		if self.oldkeyx!="" and self.oldkeyx!=self.keyx:
			cmd=["xdotool","keyup",self.oldkeyx]
			subprocess.run(cmd)
		if y!=self.keyy and self.keyy!="":
			cmd=["xdotool","keyup",self.keyy]
			subprocess.run(cmd)
			time.sleep(self.latency)
			self.oldkeyy=self.keyy
		if x!=self.keyx and self.keyx!="":
			cmd=["xdotool","keyup",self.keyx]
			subprocess.run(cmd)
			time.sleep(self.latency)
			self.oldkeyx=self.keyx
		self.keyx=x
		self.keyy=y
	#def setKeys

	def setLatency(self,latency):
		self.latency=latency
	#def setLatency
#class pressedStick

class zxButton(QPushButton):
	def __init__(self,text="space",parent=None):
		super (zxButton,self).__init__("",parent)
		self.setText(text)
		self.installEventFilter(self)
		self.setAttribute(Qt.WA_AcceptTouchEvents)
		self.setAutoRepeat(True)
		self.pressedBtn=pressedBtn()
		self.pressedBtn.setKey(self.text())
		self.css="border:3px outset silver;margin:3px;background-color:grey;color:white"
		self.pressedCss="border:3px inset silver;margin:3px;background-color:grey;color:red"
		self.setStyleSheet(self.css)
	#def __init__

	def eventFilter(self,source,event):
		if event.type()==QEvent.Type.TouchBegin:
			self.setStyleSheet(self.pressedCss)
			self.pressedBtn.start()
			return True
		elif event.type()==QEvent.Type.TouchEnd:
			self.setStyleSheet(self.css)
			return True
		return False
	#def eventFilter

	def setLatency(self,latency):
		self.pressedBtn.setLatency(latency)
	#def setLatency

class cutrebuttons(QWidget):
	def __init__(self,*args):
		super().__init__()
		self.config={'fire':'space','latency':'0.1','sizeKbd':100,'marginx':100,'marginy':100}
		if len(args)>0:
			self.setKeys(args[0])
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		self.setAttribute(Qt.WA_ShowWithoutActivating)
		self.setCursor(Qt.BlankCursor)
		self.show()
	#def __init__

	def setKeys(self,config):
		for key,item in config.items():
			if (key in self.config.keys() or key.startswith("key")) and item!='':
				self.config[key]=item
		self.drawButtons()
	#def setKeys

	def _setPosition(self):
		scr=app.primaryScreen()
		w=scr.size().width()
		h=scr.size().height()
		self.move(0+self.config['marginx'],h-self.config['marginy']-self.height())
	#def _setPosition

	def drawButtons(self):
		lay=QGridLayout()
		btnFire=zxButton()
		cont=1
		width=0
		for key,item in self.config.items():
			if item=="" or key.startswith("key")==False:
				continue
			btn=zxButton(item)
			btn.setLatency(self.config['latency'])
			btn.setAttribute(Qt.WA_AcceptTouchEvents)
			btn.clicked.connect(self.eventFilter)
			btn.setFocusPolicy(Qt.NoFocus)
			btn.setAutoRepeat(True)
			if key=="fire":
				btnFire=btn
			else:
				horizontalSize=self.config['sizeKbd']/(0.5*len(self.config))+6
				if horizontalSize<btn.minimumSizeHint().width():
					horizontalSize=btn.minimumSizeHint().width()+6
				width+=horizontalSize
				btn.setFixedSize(horizontalSize,btn.sizeHint().height()+15)
				lay.addWidget(btn,1,cont,1,1)
				cont+=1
		btnFire.setFixedHeight(btn.sizeHint().height()+(self.config['sizeKbd']/3))
		width+=btnFire.sizeHint().width()
		lay.addWidget(btnFire,2,0,1,cont+1)
		btnClose=zxButton("X")
		btnClose.setFixedSize(QSize(24,24))
		lay.addWidget(btnClose,0,0,1,cont+1,Qt.AlignRight)
		self.setLayout(lay)
		self.setFixedSize(width,self.config['sizeKbd'])
		self._setPosition()
	#def drawButtons
#class cutrebuttons

class cutrestick(QWidget):
	def __init__(self,*args):
		super().__init__()
		self.config={'left':'o','right':'p','up':'q','down':'a','tolerance':'25','latency':'0.1','marginx':100,'marginy':100,'sizeJoy':100}
		self.pressedStick=pressedStick()
		if len(args)>0:
			self.setKeys(args[0])
		confDir=os.path.dirname(__file__)
		self.rsrc=os.path.join(confDir,"images")
		self.setAttribute(Qt.WA_AcceptTouchEvents)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags(Qt.X11BypassWindowManagerHint)
		self.setAttribute(Qt.WA_ShowWithoutActivating)
		self.setFocusPolicy(Qt.NoFocus)
		self.setCursor(Qt.BlankCursor)
		self.installEventFilter(self)
		self.swTouch=False
		self.stick=QPushButton()
		self.stick.setAttribute(Qt.WA_AcceptTouchEvents)
		self._setImagesForButton()
		self.grabMouse()
		self.setMouseTracking(True) 
		self.drawStick()
		self.show()
		self._setPosition()
	#def __init__

	def _setImagesForButton(self):
		if os.path.isdir(self.rsrc):
			for img in os.listdir(self.rsrc):
				if img=="joyCenter.jpg":
					self.icnCenter=QtGui.QIcon(os.path.join(self.rsrc,img))
					self.stick.setIcon(self.icnCenter)
					self.stick.setIconSize(QSize(self.config['sizeJoy'],self.config['sizeJoy']))
				elif img=="joyUp.jpg":
					self.icnUp=QtGui.QIcon(os.path.join(self.rsrc,img))
				elif img=="joyDown.jpg":
					self.icnDown=QtGui.QIcon(os.path.join(self.rsrc,img))
				elif img=="joyLeft.jpg":
					self.icnLeft=QtGui.QIcon(os.path.join(self.rsrc,img))
				elif img=="joyRight.jpg":
					self.icnRight=QtGui.QIcon(os.path.join(self.rsrc,img))
				elif img=="joyUpLeft.jpg":
					self.icnUpLeft=QtGui.QIcon(os.path.join(self.rsrc,img))
				elif img=="joyDownLeft.jpg":
					self.icnDownLeft=QtGui.QIcon(os.path.join(self.rsrc,img))
				elif img=="joyDownRight.jpg":
					self.icnDownRight=QtGui.QIcon(os.path.join(self.rsrc,img))
				elif img=="joyUpRight.jpg":
					self.icnUpRight=QtGui.QIcon(os.path.join(self.rsrc,img))
	#def _setImagesForButton

	def setKeys(self,config):
		for key,item in config.items():
			if key in self.config.keys():
				self.config[key]=item
		self.pressedStick.setLatency(self.config['latency'])
	#def setKeys

	def _setPosition(self):
		scr=app.primaryScreen()
		w=scr.size().width()
		h=scr.size().height()
		self.move(w-(self.config['marginx']+self.width()),h-(self.config['marginy']+self.height()))
		self.stick.move((self.width()/2)-self.config['sizeJoy']/2,(self.height()/2)-self.config['sizeJoy']/2)
	#def _setPosition

	def drawStick(self):
		lay=QVBoxLayout()
		self.stick.setAutoRepeat(True)
		self.stick.setFixedSize(self.config['sizeJoy'],self.config['sizeJoy'])
		self.stick.setStyleSheet("border: 1px solid blue;border-radius: {}px;".format(self.config['sizeJoy']*2))
		self.stick.setFocusPolicy(Qt.NoFocus)
		lay.addWidget(self.stick)
		self.stick.move((self.width()/2)-self.config['sizeJoy'],(self.width()/2)-self.config['sizeJoy'])
		self.setLayout(lay)
	#def drawStick

	def eventFilter(self,source,event):
		if event.type()==QEvent.Type.TouchBegin:
			self.swTouch=True
		elif event.type()==QEvent.Type.MouseMove and self.swTouch:
			self._moveStick(event.x(),event.y())
		elif event.type()==QEvent.Type.MouseButtonRelease or event.type()==QEvent.Type.TouchEnd:
			self.swTouch=False
			icn=self.icnCenter
			self.stick.setIcon(icn)
			self.stick.setIconSize(QSize(self.config['sizeJoy'],self.config['sizeJoy']))
			self.pressedStick.setKeys(x="",y="")
		return False
	#def eventFilter
	
	def _moveStick(self, posx,posy):
		keyx=""
		keyy=""
		centerX=self.width()/2
		centerY=self.height()/2
		toleranceR=(self.config['sizeJoy']*int(self.config['tolerance']))/100
		toleranceL=(self.config['sizeJoy']*int(self.config['tolerance']))/100
		icn=self.icnCenter
		if posx>centerX-toleranceL and posx<centerX+toleranceR:
			keyx=""
		elif posx<centerX:
			keyx=self.config['left']
			icn=self.icnLeft
		elif posx>centerY:
			keyx=self.config['right']
			icn=self.icnRight
		if posy>centerY-toleranceL and posy<centerY+toleranceR:
			keyy=""
		elif posy<centerY:
			keyy=self.config['up']
			if keyx==self.config['right']:
				icn=self.icnUpRight
			elif keyx==self.config['left']:
				icn=self.icnUpLeft
			else:
				icn=self.icnUp
		elif posy>centerY:
			keyy=self.config['down']
			if keyx==self.config['right']:
				icn=self.icnDownRight
			elif keyx==self.config['left']:
				icn=self.icnDownLeft
			else:
				icn=self.icnDown
		self.stick.setIcon(icn)
		self.stick.setIconSize(QSize(self.config['sizeJoy'],self.config['sizeJoy']))
		self.pressedStick.setKeys(x=keyx,y=keyy)
		self.pressedStick.start()
	#def moveStick

#class cutrestick

def _parseConfig():
	confDir=os.path.dirname(__file__)
	configF=os.path.join(confDir,"./config.txt")
	config={'left':'o','right':'p','up':'q','down':'a','fire1':'space','key1':'m','key2':'Return','tolerance':'15','marginX':'100','marginY':'100','sizeJoy':'200','sizeKbd':'200'}
	contents=[]
	if os.path.isfile(configF):
		with open(configF,"r") as f:
			contents=f.readlines()
	for line in contents:
		if line.startswith("left"):
			config['left']=line.split("=")[-1].strip()
		elif line.startswith("right"):
			config['right']=line.split("=")[-1].strip()
		elif line.startswith("down"):
			config['down']=line.split("=")[-1].strip()
		elif line.startswith("up"):
			config['up']=line.split("=")[-1].strip()
		elif line.startswith("fire"):
			config['fire']=line.split("=")[-1].strip()
		elif line.startswith("key"):
			config[line.split("=")[0].strip()]=line.split("=")[-1].strip()
		elif line.startswith("tolerance"):
			config['tolerance']=line.split("=")[-1].strip()
		elif line.startswith("latency"):
			config['latency']=int(line.split("=")[-1].strip())/1000
		elif line.startswith("marginx"):
			config['marginx']=int(line.split("=")[-1].strip())
		elif line.startswith("marginy"):
			config['marginy']=int(line.split("=")[-1].strip())
		elif line.startswith("sizeJoy"):
			config['sizeJoy']=int(line.split("=")[-1].strip())
		elif line.startswith("sizeKbd"):
			config['sizeKbd']=int(line.split("=")[-1].strip())
	return config
#def parseConfig
	
#### MAIN APP ####
app=QApplication(["cutreStick"])
config=_parseConfig()
cutreStick=cutrestick(config)
cutreButtons=cutrebuttons(config)
app.exec_()
