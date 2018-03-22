#
# This is a tiny example that shows how to show live images from Nao using PyQt.
# You must have python-qt4 installed on your system.
#

import sys,time

from PyQt4.QtGui import QWidget, QImage, QApplication, \
                        QPushButton, QVBoxLayout, QLabel, QPixmap, \
                        QHBoxLayout

from naoqi import ALProxy
# To get the constants relative to the video.
import vision_definitions
                
class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        IP = "localhost"  # Replace here with your NaoQi's IP address.
        PORT = 9559
        self._cameraID = 0
        self._registerImageClient(IP, PORT)
        self.imgnum = 0
        self._bmanager = ALProxy("ALBehaviorManager", IP, PORT)
        if not self._bmanager.isBehaviorInstalled('stand_up'):
            self._bmanager.preloadBehavior('stand_up')
        self._motion = ALProxy("ALMotion", IP, PORT)
        self._memory = ALProxy("ALMemory",IP,PORT)
        self.initUI()
        
    def initUI(self):

        self.imageLabel = QLabel('Image',self)
        self.standUpButton = QPushButton('Stand Up', self)
        self.standUpButton.clicked.connect(self.handleStandUpButton)
        self.snapshotButton = QPushButton('Snapshot', self)
        self.snapshotButton.clicked.connect(self.handleSnapshotButton)
        self.walkButton = QPushButton('Forward', self)
        self.walkButton.clicked.connect(self.handleWalkButton)
        self.backButton = QPushButton('Backward', self)
        self.backButton.clicked.connect(self.handleBackButton)
        self.leftButton = QPushButton('Left', self)
        self.leftButton.clicked.connect(self.handleLeftButton)
        self.rightButton = QPushButton('Right', self)
        self.rightButton.clicked.connect(self.handleRightButton)
        hbox = QHBoxLayout()
        hbox.addWidget(self.leftButton)
        hbox.addWidget(self.walkButton)
        hbox.addWidget(self.backButton)
        hbox.addWidget(self.rightButton)        
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.imageLabel)
        vbox.addWidget(self.standUpButton)
        vbox.addWidget(self.snapshotButton)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setWindowTitle('Nao control')
        # Trigget 'timerEvent' every 100 ms.
        self.startTimer(100)
        self.show()

    def handleStandUpButton(self):
        print 'StandUp'
        x = self._memory.getData("Simulator/TorsoPosition/X")
        y = self._memory.getData("Simulator/TorsoPosition/Y")
        z = self._memory.getData("Simulator/TorsoPosition/Z")
        print "Robot Position: ", (x,y,z)
        if (self._bmanager.isBehaviorRunning('stand_up')):
            self._bmanager.stopBehavior('stand_up')
            time.sleep(1.0)
        self._bmanager.post.runBehavior('stand_up')

    def handleSnapshotButton(self):
        print 'Snapshot'
        self.image.save('img_' + format(self.imgnum, '04d') + '.png','PNG')
        self.imgnum = self.imgnum + 1

    def handleWalkButton(self):
        print 'Forward'
        x = self._memory.getData("Simulator/TorsoPosition/X")
        y = self._memory.getData("Simulator/TorsoPosition/Y")
        z = self._memory.getData("Simulator/TorsoPosition/Z")
        print "Robot Position: ", (x,y,z)
        self._motion.post.walkTo(0.5, 0.0, 0.0)
        
    def handleBackButton(self):
        print 'Backward'
        x = self._memory.getData("Simulator/TorsoPosition/X")
        y = self._memory.getData("Simulator/TorsoPosition/Y")
        z = self._memory.getData("Simulator/TorsoPosition/Z")
        print "Robot Position: ", (x,y,z)
        self._motion.post.walkTo(-0.5, 0.0, 0.0)
        
    def handleLeftButton(self):
        print 'Left'
        x = self._memory.getData("Simulator/TorsoPosition/X")
        y = self._memory.getData("Simulator/TorsoPosition/Y")
        z = self._memory.getData("Simulator/TorsoPosition/Z")
        print "Robot Position: ", (x,y,z)
        self._motion.post.walkTo(0.0, 0.0, 1.57)
        
    def handleRightButton(self):
        print 'Right'
        x = self._memory.getData("Simulator/TorsoPosition/X")
        y = self._memory.getData("Simulator/TorsoPosition/Y")
        z = self._memory.getData("Simulator/TorsoPosition/Z")
        print "Robot Position: ", (x,y,z)
        self._motion.post.walkTo(0.0, 0.0, -1.57)
        
    def _updateImage(self):
        """
        Retrieve a new image from Nao.
        """
        alImage = self._videoProxy.getImageRemote(self._imgClient)
        self.image = QImage(alImage[6],           # Pixel array.
							alImage[0],           # Width.
							alImage[1],           # Height.
							QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(self.image)
        self.imageLabel.setPixmap(pixmap)
        
    def timerEvent(self, event):
        """
        Called periodically. Retrieve a nao image, and update the widget.
        """
        self._updateImage()
        self.update()


    def __del__(self):
        """
        When the widget is deleted, we unregister our naoqi video module.
        """
        self._unregisterImageClient()

    def _registerImageClient(self, IP, PORT):
        """
        Register our video module to the robot.
        """
        self._videoProxy = ALProxy("ALVideoDevice", IP, PORT)
        resolution = vision_definitions.kQVGA  # 320 * 240
        colorSpace = vision_definitions.kRGBColorSpace
        self._imgClient = self._videoProxy.subscribe("_client", resolution, colorSpace, 5)

        # Select camera.
        self._videoProxy.setParam(vision_definitions.kCameraSelectID,
                                  self._cameraID)

    def _unregisterImageClient(self):
        """
        Unregister our naoqi video module.
        """
        if self._imgClient != "":
            self._videoProxy.unsubscribe(self._imgClient)

def main():

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
