import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider
from PySide2.QtGui import QPainter, QPaintEvent, QPen
from PySide2 import QtCore
from PySide2.QtCore import QTimer, QTime

class monPainter(QWidget):
    def __init__(self, parent=None):
        super(monPainter, self).__init__(parent)
        currentTime= QTime.currentTime()
        self.sec= currentTime.second()
        self.hour= currentTime.hour()
        self.min= currentTime.minute()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.runTimer)
        print(currentTime)

    def runTimer(self):
        self.sec += 1
        if self.sec == 60:          # >= 60
            self.min += 1           # = self.min+ (self.sec/60)
            self.sec = 0            # = self.sec%60
            if self.min == 60:      # >= 60
                self.hour += 1      # = self.min + (self.min/60)
                self.min = 0        # = self.min % 60
        self.update()
        print(self.hour, self.min, self.sec)

    def modifTimer(self, val):
        self.timer.setInterval (val)
        self.timer.start()

    def paintEvent(self, event:QPaintEvent):
        p = QPainter(self)
        p.setBrush(QtCore.Qt.blue)
        p.drawRect(10,10,self.width()-20, self.height()-20)
        p.setBrush(QtCore.Qt.yellow)
        p.drawEllipse(20,20,self.width()-40, self.height()-40)

        p.save()
        p.translate(self.width()/2, self.height()/2)        # permet de centrer l'aiguille
        p.save()
        p.save()
        p.rotate(270 + (360/60)*self.sec)
        penSec = QPen(QtCore.Qt.black, 1)
        p.setPen(penSec)
        p.drawLine(0,0,(self.width()-40)/3,0)
        p.restore()

        p.rotate(270 + (360/60)*self.min)
        penMin = QPen(QtCore.Qt.black, 3)
        p.setPen(penMin)
        p.drawLine(0,0,(self.width()-40)/3,0)
        p.restore()

        p.rotate(270 + (360/12)*(self.hour) + ((360/60)*(self.min))/30)         # formule a trouver pour avoir une aiguille qui tourne progressivement
        penHour = QPen(QtCore.Qt.black, 5)
        p.setPen(penHour)
        p.drawLine(0, 0, (self.width()-40)/5, 0)
        p.restore()

        p.setBrush(QtCore.Qt.magenta)
        p.drawEllipse((self.width()/2)-20, (self.height()/2)-20, 40,40)


class fenetrePrincipale(QWidget):
    def __init__(self, parent=None):
        super(fenetrePrincipale, self).__init__(parent)

        self.setMinimumSize(400,400)
        self.compteur = monPainter()
        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(1,1000)

        layout = QVBoxLayout()
        layout.addWidget(self.compteur)
        layout.addWidget(self.slider)

        # set dialog layout
        self.setLayout(layout)

        self.slider.valueChanged.connect(self.compteur.modifTimer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fen = fenetrePrincipale()
    fen.show()
    sys.exit(app.exec_())