###### UI
from maya import OpenMayaUI as omui
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from shiboken import wrapInstance
from sys import path as pythonPath
import mooCapTransfer as mo
import pymel.core as pm

reload(mo)

hip = []
newHip = []

jointList = []
newJointList = []

def getMayaWin():
	#obtain a reference to the maya window
	mayaWinPtr = omui.MQtUtil.mainWindow()
	mayaWin = wrapInstance(long(mayaWinPtr), QWidget)

def loadUI(uiName):
	"""Returns QWidget with the UI"""
	# object to load ui files
	loader = QUiLoader()
	# file name of the ui created in Qt Designer
	# directory name (we will update this until we find the file)
	dirIconShapes = ""
	# buffer to hold the XML we are going to load
	buff = None
	# search in each path of the interpreter
	for p in pythonPath:
		fname = p + '/' + uiName
		uiFile = QFile(fname)
		# if we find the "ui" file
		if uiFile.exists():
			# the directory where the UI file is
			dirIconShapes = p
			uiFile.open(QFile.ReadOnly)
			# create a temporary array so we can tweak the XML file
			buff = QByteArray( uiFile.readAll() )
			uiFile.close()
			# the filepath where the ui file is: p + uiname
			break
	else:
		print 'UI file not found'
	# fix XML
	fixXML(buff, p)
	qbuff = QBuffer()
	qbuff.open(QBuffer.ReadOnly|QBuffer.WriteOnly)
	qbuff.write(buff)
	qbuff.seek(0)
	ui = loader.load(qbuff, parentWidget = getMayaWin())
	ui.path = p
	return ui
	
def fixXML(qbyteArray, path):
	# first replace forward slashes for backslashes
	if path[-1] != '/':
		path = path + '/'
	path = path.replace("/","\\")

	# construct whole new path with <pixmap> at the begining
	tempArr = QByteArray( "<pixmap>" + path + "\\")

	# search for the word <pixmap>
	lastPos = qbyteArray.indexOf("<pixmap>", 0)
	while ( lastPos != -1 ):
		qbyteArray.replace(lastPos,len("<pixmap>"), tempArr)
	lastPos = qbyteArray.indexOf("<pixmap>", lastPos+1)
	return

#################################################################

class UIController(QObject):
    def __init__(this, UI):
    	QObject.__init__(this)
        #Connecting
        #print "test"
        
        UI.upButton1.clicked.connect(this.upButton1Func)
        UI.upButton2.clicked.connect(this.upButton2Func)  
         
        UI.downButton1.clicked.connect(this.Down1Clicked)   
        UI.downButton2.clicked.connect(this.Down2Clicked) 
          
        UI.deleteButton1.clicked.connect(this.delButton1)
        UI.deleteButton2.clicked.connect(this.delButton2)  
         
        UI.smallWindowLeft.returnPressed.connect(this.changeRoot)
        UI.smallWindowRight.returnPressed.connect(this.changeTarget) 
          
        UI.Transfer.clicked.connect(this.runProgram)  
               
        this.UI = UI
        this.UI.show()
        
    #def showUI(this):
        #this.UI.show()
        
    #def hideUI(this):
        #this.UI.hide()
			
    def delButton1(this):
        
    	currentRow = this.UI.leftWindow.currentRow()
    	this.UI.leftWindow.takeItem(currentRow)
    	jointList.pop(currentRow)
    	
    def delButton2(this):
        
    	currentRow = this.UI.rightWindow.currentRow()
    	this.UI.rightWindow.takeItem(currentRow)
    	newJointList.pop(currentRow)
    	
    def upButton1Func(this):
        
        currentRow = this.UI.leftWindow.currentRow()
        
        currentRowPrint = this.UI.leftWindow.currentRow()

        currentItem = this.UI.leftWindow.takeItem(currentRow)
        
        this.UI.leftWindow.insertItem(currentRow - 1, currentItem)
        
        #selected = this.UI.leftWindow.selectedRows()
                
        #this.UI.leftWindow.setItemSelected(this, selected)

        ############### FLYTTAR JOINT I LISTAN ##############
        currentJoint = jointList[currentRow]
        jointList[currentRow] = jointList[currentRow - 1]
        jointList[currentRow - 1] = currentJoint
        
        print jointList[currentRowPrint] + "test up1"
        
        this.UI.leftWindow.setCurrentRow(currentRow - 1)
 
    def upButton2Func(this):
        
        currentRow = this.UI.rightWindow.currentRow()
        
        currentRowPrint = this.UI.leftWindow.currentRow()

        currentItem = this.UI.rightWindow.takeItem(currentRow)
        
        this.UI.rightWindow.insertItem(currentRow - 1, currentItem)
        
        #selected = this.UI.leftWindow.selectedRows()
                
        #this.UI.leftWindow.setItemSelected(this, selected)

        ############### FLYTTAR JOINT I LISTAN ##############
        currentJoint = newJointList[currentRow]
        newJointList[currentRow] = newJointList[currentRow - 1]
        newJointList[currentRow - 1] = currentJoint
        
        print jointList[currentRowPrint] + "test up2"
        
        this.UI.rightWindow.setCurrentRow(currentRow - 1)

    	
    def Down1Clicked(this):
        
        currentRow = this.UI.leftWindow.currentRow()
        
        currentRowPrint = this.UI.leftWindow.currentRow()
        
        currentItem = this.UI.leftWindow.takeItem(currentRow)
        
        this.UI.leftWindow.insertItem(currentRow + 1, currentItem)
        
        #selected = this.UI.leftWindow.selectedRows()
                
        #this.UI.leftWindow.setItemSelected(this, selected)

        ############### FLYTTAR JOINT I LISTAN ##############
        currentJoint = jointList[currentRow]
        jointList[currentRow] = jointList[currentRow + 1]
        jointList[currentRow + 1] = currentJoint
        
        print jointList[currentRowPrint] + "test, down1"
        
        this.UI.leftWindow.setCurrentRow(currentRow + 1)
		
    def Down2Clicked(this):
        
        currentRow = this.UI.rightWindow.currentRow()
        
        currentRowPrint = this.UI.leftWindow.currentRow()

        currentItem = this.UI.rightWindow.takeItem(currentRow)
        
        this.UI.rightWindow.insertItem(currentRow + 1, currentItem)
        
        #selected = this.UI.leftWindow.selectedRows()
                
        #this.UI.leftWindow.setItemSelected(this, selected)

        ############### FLYTTAR JOINT I LISTAN ##############
        currentJoint = newJointList[currentRow]
        newJointList[currentRow] = newJointList[currentRow + 1]
        newJointList[currentRow + 1] = currentJoint
        
        print jointList[currentRowPrint] + "test , down2"
        
        this.UI.rightWindow.setCurrentRow(currentRow + 1)

    def changeRoot(this):
        del hip[:]
        hip.append(this.UI.smallWindowLeft.text())
        mo.listNodes(pm.PyNode(hip[0]), jointList)
                
        for amountOfJoints in jointList:
            this.UI.leftWindow.addItem(str(amountOfJoints))
            
    def changeTarget(this):
        del newHip[:]
        newHip.append(this.UI.smallWindowRight.text())
        mo.listNodes(pm.PyNode(newHip[0]), newJointList)
        newJointList.pop(9)
        newJointList.pop(14)
    
        for amountOfJoints in newJointList:
            this.UI.rightWindow.addItem(str(amountOfJoints))
            
    def runProgram(this):
        mo.main(jointList, newJointList, pm.PyNode(hip[0]), pm.PyNode(newHip[0]))
        