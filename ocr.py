import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QRubberBand, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QEvent, QObject, QRect, QPoint
from PyQt5.QtGui import QPixmap, QScreen 

class OcrWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.UI()
        #to save mouse position
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0

    def UI(self):
        button_style = "color: rgb(255, 255, 255);" \
                       "background-color: rgba(6, 104, 249, 255);" \
                       "border-color: rgba(151, 222, 247, 50);" \
                       "border-width: 1px;" \
                       "border-radius: 5px;"
    
        widget_style = "border-color: rgba(255, 0, 0, 255);" \
                       "border-style: solid;" \
                       "border-width: 2px;" \
                       "border-radius: 2px;" \
                       "background-color: rgba(255, 255, 255, 2);"
        # Instance of a button
        button = QPushButton("close")
        button.setFixedSize(85, 30)
        button.setStyleSheet(button_style)

        #close window
        button.clicked.connect(self.close)
        
        #Instance of horizontal part of the window
        HLayout = QHBoxLayout()
        HLayout.addStretch(1)
        HLayout.addWidget(button)
        HLayout.addStretch(1)
        
        #Instance of vertical part of the window
        vLayout = QVBoxLayout()
        vLayout.addStretch(1)
        vLayout.addLayout(HLayout)

        #Create a box widget
        cLayout = QWidget(self)
        cLayout.setLayout(vLayout)
        cLayout.setStyleSheet(widget_style)
        cLayout.setMouseTracking(True)
        cLayout.installEventFilter(self)
        cLayout.setFixedSize(400,200)

        #set window with the new box window
        self.setCentralWidget(cLayout)

    #change icon of mouse when it is released
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.ArrowCursor)

    #changes coordenates to move window later
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pos_x = event.pos().x()
            self.mouse_pos_y = event.pos().y()

    #move window
    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        #use move event
        if event.type() == QEvent.MouseMove:
            #only move when clicked
            if event.buttons() & Qt.LeftButton:
                QApplication.setOverrideCursor(Qt.SizeAllCursor)
                #claculates new coordinates 
                self.move(event.globalPos().x() - self.mouse_pos_x,
                          event.globalPos().y() - self.mouse_pos_y,)
            else: return False
        else: return False
    
        return True

def main():
    app = QApplication(sys.argv)
    window = OcrWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
