import sys
import cv2
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QRubberBand, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QEvent, QObject, QRect, QPoint
from PyQt5.QtGui import QPixmap, QScreen 
from PIL import ImageGrab, Image
from log import logWindow
from textblob import TextBlob

import numpy as np

class OcrWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ocr")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.UI()
        #to save mouse position
        self.mouse_pos_x = 0
        self.mouse_pos_y = 0
        self.is_resizing = False
        self.resize_margin = 10  # Define margin for resizing window

        self.log_window = logWindow() 

    

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
        # Instance of a button to close
        button = QPushButton("close")
        button.setFixedSize(85, 30)
        button.setStyleSheet(button_style)

        #close window
        button.clicked.connect(self.close)

        button2 = QPushButton("Capture")
        button2.setFixedSize(85, 30)
        button2.setStyleSheet(button_style)

        button2.clicked.connect(self.screenShot)
        
        #Instance of horizontal part of the window
        HLayout = QHBoxLayout()
        HLayout.addStretch(1)
        HLayout.addWidget(button)
        HLayout.addWidget(button2)
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
       

        #set window with the new box window
        self.setCentralWidget(cLayout)

    #change icon of mouse when it is released
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.is_resizing = False


    #changes coordenates to move window later
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pos_x = event.pos().x()
            self.mouse_pos_y = event.pos().y()
        
         # Check if it's within the resize area
        if (self.width() - event.pos().x() <= self.resize_margin) or (self.height() - event.pos().y() <= self.resize_margin):
            self.is_resizing = True
            QApplication.setOverrideCursor(Qt.SizeFDiagCursor)  # Resize cursor

    #move window
    def eventFilter(self, source: QObject, event: QEvent) -> bool:
          # Only process mouse move events
        if event.type() == QEvent.MouseMove:
            if self.is_resizing:
                # Resize window based on mouse movement
                dx = event.pos().x() - self.mouse_pos_x
                dy = event.pos().y() - self.mouse_pos_y
                self.resize(self.width() + dx, self.height() + dy)
                self.mouse_pos_x = event.pos().x()
                self.mouse_pos_y = event.pos().y()
            elif event.buttons() & Qt.LeftButton:
                QApplication.setOverrideCursor(Qt.SizeAllCursor)
                self.move(event.globalPos().x() - self.mouse_pos_x,
                        event.globalPos().y() - self.mouse_pos_y)
            return True  # We handled the event
        else:
            return False

    #Send text captured to log
    def SendText(self, img):
        #transform pil image into cv for preprocessing
        img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) # Convert PIL to OpenCV (BGR)

        processed = self.morphological_operations(img_cv2)  #Separate text in rows

        pil_image = Image.fromarray(processed)  # Convert back to PIL for Tesseract
        ocr_result = pytesseract.image_to_string(pil_image,  lang='spa', config='--psm 6')
        print(ocr_result)
        
        if ocr_result == "":
            print("There is no text")
        else:
            if self.log_window:
                self.log_window.add_text(ocr_result)
                self.log_window.show()
         
       
    
    def screenShot(self):
        # get geometry of the central widget without borders
        widget_geom = self.centralWidget().geometry()

        #Turn local coordenates from the central widget to global
        topLeft = self.centralWidget().mapToGlobal(widget_geom.topLeft())
        bottomRight = self.centralWidget().mapToGlobal(widget_geom.bottomRight())

        # get coordenates from the screen
        x1, y1 = topLeft.x(), topLeft.y()
        x2, y2 = bottomRight.x(), bottomRight.y()

        # screenshot insede the limits
        im = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        ocr_text = self.SendText(im)

    
    def morphological_operations(self, img):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # Define a small kernel
        processed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)  # Apply closing to fill gaps
        return processed

    
 



def main():
    app = QApplication(sys.argv)
    window = OcrWindow()
    window.resize(400, 200)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
